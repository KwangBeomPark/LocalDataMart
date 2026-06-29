import sys
import uuid
from pathlib import Path
import pandas as pd

from app.logger_setup import MartLogger
from app.config_loader import ConfigLoader
from app.file_scanner import FileScanner
from app.excel_reader import ExcelReader
from app.transformer import Transformer
from app.report_generator import ReportGenerator
from app.validator import Validator

def main():
    # 1. 고유 실행 ID 생성
    run_id = str(uuid.uuid4())[:8]
    
    # 2. 로거 초기화
    logger = MartLogger(log_dir="sample_workspace/99_Logs")
    logger.info(f"=== Finance DataMart Tool MVP Start (Run ID: {run_id}) ===")
    
    try:
        # 3. 설정 파일 로드
        logger.info("Loading config.xlsx...")
        config_loader = ConfigLoader(config_path="sample_workspace/90_Config/config.xlsx")
        try:
            df_source, df_mapping, df_report = config_loader.load_all_configs()
            logger.log_validation("Config_Loading", "PASS", "Successfully loaded and validated config.xlsx")
        except Exception as ce:
            err_msg = f"Config loading error: {ce}"
            logger.error(err_msg, ce)
            logger.log_validation("Config_Loading", "FAIL", err_msg)
            sys.exit(1)
        
        # 4. active = 'Y' 인 데이터 소스 그룹 처리
        active_sources = df_source[df_source["active"] == "Y"]
        if active_sources.empty:
            err_msg = "No active data groups found in Source_Config."
            logger.warning(err_msg)
            logger.log_validation("Active_Source_Validation", "FAIL", err_msg)
            return

        clean_tables = {}  # 데이터그룹별 Clean DataFrame 캐시
        active_reports = df_report[df_report["active"] == "Y"]
        clean_output_dir = Path("sample_workspace/03_Clean_Table")
        report_output_dir = Path("sample_workspace/04_Report_View")
        clean_output_dir.mkdir(parents=True, exist_ok=True)
        report_output_dir.mkdir(parents=True, exist_ok=True)
        expected_clean_paths = [
            clean_output_dir / f"{source_row['data_group'].lower()}_clean.csv"
            for _, source_row in active_sources.iterrows()
        ]
        expected_report_paths = []
        for _, report_row in active_reports.iterrows():
            output_file = str(report_row["output_file"]).strip()
            if Path(output_file).name != output_file or not output_file.lower().endswith(".csv"):
                raise ValueError(
                    f"Invalid output_file '{output_file}' for Report View '{report_row['view_name']}'. "
                    "Report output must be a CSV filename without folder path."
                )
            expected_report_paths.append(report_output_dir / output_file)
        for output_path in expected_clean_paths + expected_report_paths:
            if output_path.exists():
                output_path.unlink()
        raw_stats = {}
        
        # 5. 각 데이터 그룹 순회 (Sales_Closing 등)
        for _, source_row in active_sources.iterrows():
            data_group = source_row["data_group"]
            folder_path = source_row["folder_path"]
            file_pattern = source_row["file_pattern"]
            sheet_name = source_row["sheet_name"]
            header_row = int(source_row["header_row"])
            
            logger.info(f"Processing data group: {data_group} (Path: {folder_path})")
            
            # 파일 스캔
            try:
                files = FileScanner.scan_files(folder_path, file_pattern)
                logger.info(f"Scanned {len(files)} files in {folder_path}")
            except Exception as e:
                logger.error(f"Error scanning files for {data_group}: {e}", e)
                logger.log_refresh(run_id, data_group, "", "FAIL", 0, "", f"Scanning error: {e}")
                continue

            if not files:
                logger.warning(f"No files found for data group {data_group} matching pattern {file_pattern}")
                logger.log_refresh(run_id, data_group, "", "SUCCESS", 0, "", "No files matched pattern")
                continue

            # 파일 읽기 및 변환
            transformer = Transformer(df_mapping)
            group_rules = transformer.get_group_mappings(data_group)
            required_raw_cols = group_rules[group_rules["required"] == "Y"]["raw_column"].tolist()
            
            # Reconciliation을 위한 Raw 통계 수집 준비
            group_mapping = df_mapping[(df_mapping["data_group"] == data_group) & (df_mapping["keep"] == "Y")]
            measure_cols = group_mapping[(group_mapping["role"] == "measure") | (group_mapping["aggregation"] == "sum")]
            raw_stats[data_group] = {
                "total_rows": 0,
                "measure_sums": {row["raw_column"]: 0.0 for _, row in measure_cols.iterrows()}
            }
            
            transformed_dfs = []
            
            for file_path in files:
                logger.info(f"Reading file: {file_path.name}")
                try:
                    # 엑셀 시트 읽기
                    raw_df = ExcelReader.read_sheet(file_path, sheet_name, header_row)
                    
                    # 통계 누계
                    raw_stats[data_group]["total_rows"] += len(raw_df)
                    for raw_col in raw_stats[data_group]["measure_sums"].keys():
                        if raw_col in raw_df.columns:
                            raw_stats[data_group]["measure_sums"][raw_col] += pd.to_numeric(raw_df[raw_col], errors="coerce").fillna(0.0).sum()
                    
                    # 필수 컬럼 사전 검증
                    missing_cols = Validator.validate_raw_columns(raw_df, required_raw_cols, file_path.name)
                    if missing_cols:
                        err_msg = f"Missing required columns: {missing_cols}"
                        logger.error(f"Validation failed for {file_path.name}: {err_msg}")
                        logger.log_refresh(run_id, data_group, file_path.name, "FAIL", 0, "", err_msg)
                        continue

                    # 데이터 변환
                    clean_df = transformer.transform_single_file(raw_df, file_path, source_row)
                    transformed_dfs.append(clean_df)
                    
                    logger.info(f"Successfully processed {file_path.name} ({len(clean_df)} rows)")
                    logger.log_refresh(
                        run_id, data_group, file_path.name, "SUCCESS", 
                        len(clean_df), "", f"Processed file successfully"
                    )
                except Exception as e:
                    logger.error(f"Error processing file {file_path.name}: {e}", e)
                    logger.log_refresh(run_id, data_group, file_path.name, "FAIL", 0, "", str(e))

            # 데이터 병합 및 Clean Table CSV 저장
            if transformed_dfs:
                combined_df = Transformer.combine_dataframes(transformed_dfs)
                clean_tables[data_group] = combined_df
                
                # 파일명 생성: 데이터 그룹명을 소문자화하고 _clean.csv 접미사 추가
                clean_filename = f"{data_group.lower()}_clean.csv"
                clean_table_path = clean_output_dir / clean_filename
                
                combined_df.to_csv(clean_table_path, index=False, encoding="utf-8-sig")
                
                logger.info(f"Clean Table created: {clean_table_path.name} (Total {len(combined_df)} rows)")
                logger.log_refresh(
                    run_id, data_group, "", "SUCCESS", 
                    len(combined_df), clean_table_path.name, "Combined Clean Table saved"
                )
            else:
                logger.warning(f"No data successfully processed for data group: {data_group}")

        # 6. Report_View 생성
        report_generator = ReportGenerator(output_dir=str(report_output_dir))
        
        # Report_View 설정에 대한 조기 무결성 검증 수행 및 기록
        report_config_errors = []
        for _, report_row in active_reports.iterrows():
            view_name = report_row["view_name"]
            try:
                report_generator.validate_report_config(report_row, clean_tables)
                logger.log_validation(
                    f"Report_View_Config:{view_name}", "PASS", 
                    f"Configuration for Report View '{view_name}' is valid."
                )
            except Exception as e:
                err_msg = f"Report View '{view_name}' configuration is invalid: {e}"
                logger.log_validation(f"Report_View_Config:{view_name}", "FAIL", err_msg)
                logger.error(err_msg)
                report_config_errors.append(err_msg)

        if report_config_errors:
            raise RuntimeError(
                f"Report_View configuration validation failed with {len(report_config_errors)} error(s). "
                f"Check validation_log.csv or console output for details."
            )
            
        for _, report_row in active_reports.iterrows():
            view_name = report_row["view_name"]
            source_table = report_row["source_table"]  # 예: sales_closing_clean
            output_file = report_row["output_file"]
            
            logger.info(f"Generating Report View: {view_name} (Source: {source_table})")
            
            # 소스 테이블 DataFrame 매칭
            # Source Config의 데이터 그룹명(예: Sales_Closing)을 소문자화하고 _clean을 붙인 이름을 활용
            matched_group = None
            for group_name in clean_tables.keys():
                if f"{group_name.lower()}_clean" == source_table:
                    matched_group = group_name
                    break
            
            if matched_group is None:
                err_msg = f"Source Clean Table DataFrame not found for table name '{source_table}'"
                logger.error(err_msg)
                logger.log_refresh(run_id, "", "", "FAIL", 0, output_file, err_msg)
                continue
                
            clean_df = clean_tables[matched_group]
            
            try:
                summary_df = report_generator.generate_view(clean_df, report_row)
                report_path = report_generator.save_report(summary_df, output_file)
                
                logger.info(f"Report View created: {output_file} ({len(summary_df)} rows)")
                logger.log_refresh(
                    run_id, matched_group, "", "SUCCESS", 
                    len(summary_df), output_file, "Report View saved"
                )
            except Exception as e:
                logger.error(f"Error generating Report View {view_name}: {e}", e)
                logger.log_refresh(run_id, matched_group, "", "FAIL", 0, output_file, str(e))

        # 7. 최종 산출물 검증 및 validation_log.csv 생성
        logger.info("Starting validation of generated outputs...")
        validator = Validator()
        # Config 기준으로 생성되어야 하는 모든 Clean/Report 산출물을 검증
        validation_results = validator.validate_outputs(expected_clean_paths, expected_report_paths)

        # 8. 원본(Raw Excel)과 결과(Clean Table) 대조 검증 (Reconciliation)
        logger.info("Starting reconciliation checks (Raw vs Clean)...")
        try:
            recon_results = validator.validate_reconciliation(active_sources, df_mapping, clean_tables, raw_stats)
            validation_results.extend(recon_results)
        except Exception as recon_err:
            recon_fail_msg = f"Fatal error during reconciliation: {recon_err}"
            logger.error(recon_fail_msg)
            validation_results.append({
                "step": "Reconciliation_Overall",
                "status": "FAIL",
                "message": recon_fail_msg
            })
        
        for res in validation_results:
            logger.log_validation(res["step"], res["status"], res["message"])
            if res["status"] == "PASS":
                logger.info(f"Validation PASS: {res['message']}")
            else:
                logger.warning(f"Validation FAIL: {res['message']}")

        if any(res["status"] != "PASS" for res in validation_results):
            raise RuntimeError("One or more output validation checks failed.")

        logger.info("=== Finance DataMart Tool MVP Finished Successfully ===")

    except Exception as e:
        logger.error(f"Critical pipeline error: {e}", e)
        logger.log_validation("Overall_Pipeline", "FAIL", f"Fatal error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
