from pathlib import Path
import pandas as pd
from typing import List, Dict

class Validator:
    @staticmethod
    def validate_raw_columns(df: pd.DataFrame, required_columns: List[str], file_name: str) -> List[str]:
        """Raw DataFrame에 필수 컬럼들이 존재하는지 검증합니다.
        
        Returns:
            List[str]: 누락된 필수 컬럼 목록
        """
        missing = [col for col in required_columns if col not in df.columns]
        return missing

    @staticmethod
    def check_file_exists_and_not_empty(file_path: Path) -> bool:
        """파일이 실제로 존재하고 크기가 0보다 큰지 검증합니다."""
        return file_path.exists() and file_path.stat().st_size > 0

    def validate_outputs(self, clean_table_paths: List[Path], report_view_paths: List[Path]) -> List[dict]:
        """생성된 최종 산출물들의 존재 여부 및 정상 생성 여부를 검증하고 결과를 반환합니다."""
        results = []
        
        # 1. Clean Table 검증
        for path in clean_table_paths:
            if self.check_file_exists_and_not_empty(path):
                results.append({
                    "step": "Clean_Table_Validation",
                    "status": "PASS",
                    "message": f"Clean Table successfully created at: {path.name}"
                })
            else:
                results.append({
                    "step": "Clean_Table_Validation",
                    "status": "FAIL",
                    "message": f"Clean Table is missing or empty at: {path.name}"
                })

        # 2. Report View 검증
        for path in report_view_paths:
            if self.check_file_exists_and_not_empty(path):
                results.append({
                    "step": "Report_View_Validation",
                    "status": "PASS",
                    "message": f"Report View successfully created at: {path.name}"
                })
            else:
                results.append({
                    "step": "Report_View_Validation",
                    "status": "FAIL",
                    "message": f"Report View is missing or empty at: {path.name}"
                })
                
        return results

    def validate_reconciliation(self, active_sources: pd.DataFrame, df_mapping: pd.DataFrame, clean_tables: Dict[str, pd.DataFrame], raw_stats: Dict[str, dict] = None) -> List[dict]:
        """생성된 Clean Table과 원본 Excel 파일 간의 Row Count 및 수치(measure) 합계를 대조 검증합니다."""
        results = []
        from app.file_scanner import FileScanner
        from app.excel_reader import ExcelReader
        
        for _, source_row in active_sources.iterrows():
            data_group = source_row["data_group"]
            folder_path = source_row["folder_path"]
            file_pattern = source_row["file_pattern"]
            sheet_name = source_row["sheet_name"]
            header_row = int(source_row["header_row"])
            
            # Clean Table 로드 확인
            if data_group not in clean_tables:
                results.append({
                    "step": f"Reconciliation:{data_group}",
                    "status": "FAIL",
                    "message": f"Clean Table for group '{data_group}' is not generated. Cannot perform reconciliation."
                })
                continue
                
            clean_df = clean_tables[data_group]
            
            # Mapping 필터링 (해당 data_group 전용)
            group_mapping = df_mapping[(df_mapping["data_group"] == data_group) & (df_mapping["keep"] == "Y")]
            measure_cols = group_mapping[(group_mapping["role"] == "measure") | (group_mapping["aggregation"] == "sum")]
            raw_sums = {row["raw_column"]: 0.0 for _, row in measure_cols.iterrows()}
            
            raw_row_sum = 0
            read_success = True

            # 만약 사전에 추출된 raw_stats 캐시 정보가 제공된다면 디스크 리딩(I/O) 생략
            if raw_stats and data_group in raw_stats:
                raw_row_sum = raw_stats[data_group].get("total_rows", 0)
                cached_sums = raw_stats[data_group].get("measure_sums", {})
                for raw_col in raw_sums.keys():
                    raw_sums[raw_col] = cached_sums.get(raw_col, 0.0)
            else:
                # Raw 파일 스캔 및 데이터 수집 (Fallback)
                try:
                    files = FileScanner.scan_files(folder_path, file_pattern)
                except Exception as e:
                    results.append({
                        "step": f"Reconciliation:{data_group}",
                        "status": "FAIL",
                        "message": f"Failed to scan folder '{folder_path}': {e}"
                    })
                    continue
                    
                if not files:
                    results.append({
                        "step": f"Reconciliation:{data_group}",
                        "status": "FAIL",
                        "message": f"No Raw Excel files found in '{folder_path}' matching pattern '{file_pattern}'"
                    })
                    continue
                    
                # Raw 데이터 로드 및 합산 (읽기 전용)
                for file_path in files:
                    try:
                        df_raw = ExcelReader.read_sheet(file_path, sheet_name, header_row)
                        raw_row_sum += len(df_raw)
                        
                        for raw_col in raw_sums.keys():
                            if raw_col in df_raw.columns:
                                # NaN 값을 0으로 채우고 수치 변환
                                raw_sums[raw_col] += pd.to_numeric(df_raw[raw_col], errors="coerce").fillna(0.0).sum()
                    except Exception as e:
                        results.append({
                            "step": f"Reconciliation:{data_group}",
                            "status": "FAIL",
                            "message": f"Failed to read raw file '{file_path.name}': {e}"
                        })
                        read_success = False
                        break
                    
            if not read_success:
                continue
                
            # 1. Row Count 검증
            clean_row_count = len(clean_df)
            if raw_row_sum == clean_row_count:
                results.append({
                    "step": f"Reconciliation_RowCount:{data_group}",
                    "status": "PASS",
                    "message": f"Row count matched. Raw total: {raw_row_sum} rows vs Clean: {clean_row_count} rows."
                })
            else:
                results.append({
                    "step": f"Reconciliation_RowCount:{data_group}",
                    "status": "FAIL",
                    "message": f"Row count mismatched! Raw total: {raw_row_sum} rows vs Clean: {clean_row_count} rows. (Difference: {raw_row_sum - clean_row_count})"
                })
                
            # 2. 필수 컬럼 결측치 검증
            required_cols = group_mapping[group_mapping["required"] == "Y"]
            for _, map_row in required_cols.iterrows():
                std_col = map_row["standard_column"]
                raw_col = map_row["raw_column"]
                if std_col in clean_df.columns:
                    null_count = clean_df[std_col].isna().sum()
                    # 문자열 빈값('')도 결측으로 간주
                    empty_str_count = 0
                    if clean_df[std_col].dtype == "object":
                        empty_str_count = (clean_df[std_col].astype(str).str.strip() == "").sum()
                    total_missing = null_count + empty_str_count
                    
                    if total_missing == 0:
                        results.append({
                            "step": f"Reconciliation_NullCheck:{data_group}:{std_col}",
                            "status": "PASS",
                            "message": f"Required column '{std_col}' has 0 null/empty values."
                        })
                    else:
                        results.append({
                            "step": f"Reconciliation_NullCheck:{data_group}:{std_col}",
                            "status": "FAIL",
                            "message": f"Required column '{std_col}' (mapped from '{raw_col}') contains {total_missing} null/empty value(s) in Clean Table."
                        })
                        
            # 3. measure 컬럼 합계 검증
            for _, map_row in measure_cols.iterrows():
                std_col = map_row["standard_column"]
                raw_col = map_row["raw_column"]
                
                if std_col in clean_df.columns:
                    clean_sum = pd.to_numeric(clean_df[std_col], errors="coerce").fillna(0.0).sum()
                    raw_sum = raw_sums[raw_col]
                    
                    # 허용 오차 0.01 대조
                    diff = abs(raw_sum - clean_sum)
                    if diff <= 0.01:
                        results.append({
                            "step": f"Reconciliation_SumCheck:{data_group}:{std_col}",
                            "status": "PASS",
                            "message": f"Sum matched for '{std_col}'. Raw: {raw_sum:.2f} vs Clean: {clean_sum:.2f} (diff: {diff:.4f})."
                        })
                    else:
                        results.append({
                            "step": f"Reconciliation_SumCheck:{data_group}:{std_col}",
                            "status": "FAIL",
                            "message": f"Sum mismatched for '{std_col}' (mapped from '{raw_col}')! Raw: {raw_sum:.2f} vs Clean: {clean_sum:.2f} (diff: {diff:.2f})."
                        })
                        
        return results
