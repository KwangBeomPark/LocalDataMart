import os
import re
import sys
import pandas as pd
from pathlib import Path
from datetime import datetime


PROJECT_ROOT = Path(__file__).resolve().parent.parent


class PreReleaseChecker:
    def __init__(self):
        self.project_root = PROJECT_ROOT
        self.workspace_dir = self.project_root / "sample_workspace"
        self.log_dir = self.workspace_dir / "99_Logs"
        self.error_log = self.log_dir / "error_log.txt"
        self.validation_log = self.log_dir / "validation_log.csv"
        self.refresh_log = self.log_dir / "refresh_log.csv"
        self.check_log_file = self.log_dir / "pre_release_check_log.txt"
        
        # 필수 산출물 파일 리스트
        self.expected_outputs = [
            self.workspace_dir / "03_Clean_Table" / "sales_closing_clean.csv",
            self.workspace_dir / "03_Clean_Table" / "ar_detail_clean.csv",
            self.workspace_dir / "04_Report_View" / "sales_by_customer.csv",
            self.workspace_dir / "04_Report_View" / "sales_by_model.csv",
            self.workspace_dir / "04_Report_View" / "sales_by_customer_model.csv",
            self.workspace_dir / "04_Report_View" / "ar_by_customer.csv",
            self.workspace_dir / "04_Report_View" / "ar_by_aging_bucket.csv",
            self.workspace_dir / "04_Report_View" / "sales_invoice_count_by_customer.csv",
            self.workspace_dir / "04_Report_View" / "ar_invoice_count_by_customer.csv",
            self.workspace_dir / "90_Config" / "column_inventory.xlsx"
        ]
        
        # 금지 기술 키워드
        self.forbidden_keywords = ["duckdb", "parquet", "pyside6", "fastapi", "flask"]
        
        # 내부 절대경로 의심 키워드
        self.traceback_keywords = ["traceback", "file \"", "c:\\users", "c:/users", "/users/", "/home/"]
        
        # 가상 Raw Excel 무결성 대상
        self.raw_excel_files = {
            self.workspace_dir / "01_Input_Raw" / "Sales_Closing" / "Sales_Closing_2026_01.xlsx": ["Invoice No", "Customer Code", "Posting Date", "Model", "Qty", "Net Sales"],
            self.workspace_dir / "01_Input_Raw" / "Sales_Closing" / "Sales_Closing_2026_02.xlsx": ["Invoice No", "Customer Code", "Posting Date", "Model", "Qty", "Net Sales"],
            self.workspace_dir / "01_Input_Raw" / "AR_Detail" / "AR_Detail_2026_01.xlsx": ["Invoice No", "Customer Code", "Posting Date", "Amount", "Aging Bucket"],
            self.workspace_dir / "01_Input_Raw" / "AR_Detail" / "AR_Detail_2026_02.xlsx": ["Invoice No", "Customer Code", "Posting Date", "Amount", "Aging Bucket"]
        }

    def sanitize_message(self, value) -> str:
        text = "" if value is None else str(value)
        replacements = [
            str(self.project_root),
            str(self.project_root).replace("\\", "/"),
            str(Path.home()),
            str(Path.home()).replace("\\", "/"),
        ]
        for path_text in replacements:
            if path_text:
                text = text.replace(path_text, "[local_path]")
        return re.sub(r"[A-Za-z]:[\\/][^\s,\")']+", "[local_path]", text)

    def run_checks(self) -> bool:
        results = []
        overall_pass = True
        
        print("=== Finance DataMart Pre-release Integrity Check Start ===")
        
        # 1. 컴파일 정상 작동 확인
        compile_pass, compile_msg = self.check_compilation()
        results.append(("Python Code Compilation Check", compile_pass, compile_msg))
        if not compile_pass:
            overall_pass = False
            
        # 2. 필수 산출물 생존 여부 검사
        outputs_pass, outputs_msg = self.check_outputs_exist()
        results.append(("Expected Output Files Check", outputs_pass, outputs_msg))
        if not outputs_pass:
            overall_pass = False
            
        # 3. 에러 로그 비어있음/무오류 검사
        err_log_pass, err_log_msg = self.check_error_log_empty()
        results.append(("Error Log Empty Check", err_log_pass, err_log_msg))
        if not err_log_pass:
            overall_pass = False
            
        # 4. 검증 로그 FAIL 검사
        valid_log_pass, valid_log_msg = self.check_validation_log_pass()
        results.append(("Validation Log Result Check", valid_log_pass, valid_log_msg))
        if not valid_log_pass:
            overall_pass = False
            
        # 5. 소스코드 금지 키워드 유입 검사
        kw_pass, kw_msg = self.check_forbidden_keywords()
        results.append(("Forbidden Technology Keyword Check", kw_pass, kw_msg))
        if not kw_pass:
            overall_pass = False
            
        # 6. 로그 내 콜스택/절대경로 노출 검사
        path_pass, path_msg = self.check_absolute_paths_in_logs()
        results.append(("Stack/Path Leak Check", path_pass, path_msg))
        if not path_pass:
            overall_pass = False
            
        # 7. Raw Excel 파일 무결성 및 구조 훼손 여부 검사
        excel_pass, excel_msg = self.check_raw_excel_integrity()
        results.append(("Raw Excel Integrity Check", excel_pass, excel_msg))
        if not excel_pass:
            overall_pass = False

        # 콘솔 요약 출력
        print("\n--- Summary ---")
        log_lines = []
        log_lines.append(f"Pre-release check run at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        log_lines.append(f"Overall Result: {'PASS' if overall_pass else 'FAIL'}\n")
        
        for name, status, msg in results:
            status_str = "PASS" if status else "FAIL"
            safe_msg = self.sanitize_message(msg)
            print(f"[{status_str}] {name}")
            print(f"       Info: {safe_msg}")
            log_lines.append(f"[{status_str}] {name} - Info: {safe_msg}")
            
        print("=========================================================")
        
        # 로그 파일 저장
        try:
            self.log_dir.mkdir(parents=True, exist_ok=True)
            with open(self.check_log_file, "w", encoding="utf-8") as f:
                f.write("\n".join(log_lines) + "\n")
        except Exception as log_err:
            print(f"Warning: Failed to write check log file: {self.sanitize_message(log_err)}")
            
        return overall_pass

    def check_compilation(self) -> tuple:
        try:
            import subprocess
            res = subprocess.run(
                [sys.executable, "-m", "compileall", "app", "scripts"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                cwd=self.project_root
            )
            if res.returncode == 0:
                return True, "No syntax or compilation errors found in 'app/' and 'scripts/'."
            else:
                return False, f"Compilation failed: {self.sanitize_message(res.stderr or res.stdout)}"
        except Exception as e:
            return False, f"Failed to run compileall: {self.sanitize_message(e)}"

    def check_outputs_exist(self) -> tuple:
        missing_files = []
        empty_files = []
        
        for file_path in self.expected_outputs:
            if not file_path.exists():
                missing_files.append(file_path.name)
            elif file_path.stat().st_size == 0:
                empty_files.append(file_path.name)
                
        if missing_files or empty_files:
            err_details = []
            if missing_files:
                err_details.append(f"Missing: {missing_files}")
            if empty_files:
                err_details.append(f"0-byte: {empty_files}")
            return False, f"Output files integrity failed. Details: {', '.join(err_details)}"
            
        return True, f"All {len(self.expected_outputs)} expected output files successfully generated and not empty."

    def check_error_log_empty(self) -> tuple:
        if not self.error_log.exists():
            return True, "No error log file found (clean state)."
            
        size = self.error_log.stat().st_size
        if size == 0:
            return True, "Error log file exists but is 0 bytes (clean state)."
            
        try:
            with open(self.error_log, "r", encoding="utf-8") as f:
                content = f.read().strip()
            if not content:
                return True, "Error log file exists but contains only whitespace (clean state)."
            # 첫 80자만 잘라서 원인 반환
            first_err = content.split("\n")[0][:80]
            return False, f"Error log is not empty! First logged error: '{self.sanitize_message(first_err)}'"
        except Exception as e:
            return False, f"Failed to read error log: {self.sanitize_message(e)}"

    def check_validation_log_pass(self) -> tuple:
        if not self.validation_log.exists():
            return False, "Validation log file is missing. Run main pipeline first."
            
        try:
            df = pd.read_csv(self.validation_log)
            if len(df) == 0:
                return False, "Validation log is empty."
                
            # 가장 마지막(최신) 실행 시각(run_datetime) 행들만 필터링
            latest_time = df["run_datetime"].iloc[-1]
            df_latest = df[df["run_datetime"] == latest_time]
            
            # status 컬럼에 FAIL이 존재하는지 확인
            if "status" in df_latest.columns:
                fails = df_latest[df_latest["status"].str.upper() == "FAIL"]
                if len(fails) > 0:
                    first_fail = fails.iloc[0]
                    return False, self.sanitize_message(
                        f"FAIL status found in latest validation log (at {latest_time}): "
                        f"Step '{first_fail.get('step')}' failed. Msg: {first_fail.get('message')}"
                    )
                return True, f"All validation checks in the latest execution (at {latest_time}) are PASS."
            else:
                return False, "Status column missing in validation log."
        except Exception as e:
            return False, f"Failed to parse validation log: {self.sanitize_message(e)}"

    def check_forbidden_keywords(self) -> tuple:
        found_violations = []
        app_dir = self.project_root / "app"
        scripts_dir = self.project_root / "scripts"
        req_file = self.project_root / "requirements.txt"
        
        # 스캔할 파일 수집 (pre_release_check.py 본인 제외)
        files_to_check = []
        if app_dir.exists():
            files_to_check.extend([f for f in app_dir.rglob("*.py") if f.is_file()])
        if scripts_dir.exists():
            files_to_check.extend([
                f for f in scripts_dir.rglob("*.py") 
                if f.is_file() and f.name != Path(__file__).name
            ])
        if req_file.exists():
            files_to_check.append(req_file)
            
        for file_path in files_to_check:
            try:
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read().lower()
                for kw in self.forbidden_keywords:
                    # 키워드가 온전한 단어로 매칭되거나 주석 등에 박혀있는지 스캔
                    if kw in content:
                        found_violations.append(f"{file_path.name}:{kw}")
            except Exception as read_err:
                return False, f"Failed to read file {file_path.name}: {self.sanitize_message(read_err)}"
                
        if found_violations:
            return False, f"Forbidden keywords detected in codebases: {', '.join(found_violations)}"
        return True, f"Checked {len(files_to_check)} source/config files. No forbidden keywords found."

    def check_absolute_paths_in_logs(self) -> tuple:
        logs_to_check = [self.error_log, self.validation_log, self.refresh_log]
        found_leaks = []
        
        for log_path in logs_to_check:
            if not log_path.exists():
                continue
            try:
                with open(log_path, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read().lower()
                for kw in self.traceback_keywords:
                    if kw in content:
                        found_leaks.append(f"{log_path.name}:{kw}")
            except Exception as read_err:
                return False, f"Failed to read log {log_path.name}: {self.sanitize_message(read_err)}"
                
        if found_leaks:
            return False, f"Stack trace or absolute paths detected in user logs: {', '.join(found_leaks)}"
        return True, "No stack trace or absolute paths leaked in user logs."

    def check_raw_excel_integrity(self) -> tuple:
        for file_path, expected_cols in self.raw_excel_files.items():
            if not file_path.exists():
                return False, f"Raw Excel file missing: {file_path.name}"
            try:
                # pandas로 엑셀 로딩 검증
                df = pd.read_excel(file_path, sheet_name=0, header=0)
                # 컬럼 유무 확인
                missing_cols = [c for c in expected_cols if c not in df.columns]
                if missing_cols:
                    return False, f"Raw Excel '{file_path.name}' column schema is broken! Missing: {missing_cols}"
                if len(df) == 0:
                    return False, f"Raw Excel '{file_path.name}' is empty (0 rows)."
            except Exception as e:
                return False, f"Raw Excel '{file_path.name}' is corrupted or unreadable: {self.sanitize_message(e)}"
        return True, f"All {len(self.raw_excel_files)} virtual Raw Excel files have correct schemas and are readable."

def main():
    checker = PreReleaseChecker()
    success = checker.run_checks()
    if not success:
        sys.exit(1)
    sys.exit(0)

if __name__ == "__main__":
    main()
