import csv
import logging
import re
from pathlib import Path
from datetime import datetime

class MartLogger:
    def __init__(self, log_dir: str = "sample_workspace/99_Logs"):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
        self.refresh_log_path = self.log_dir / "refresh_log.csv"
        self.validation_log_path = self.log_dir / "validation_log.csv"
        self.error_log_path = self.log_dir / "error_log.txt"
        self.error_log_path.write_text("", encoding="utf-8")
        
        self._init_standard_logging()
        self._init_csv_logs()

    def _init_standard_logging(self):
        """Python 표준 logging을 설정하여 console 및 error_log.txt에 출력합니다."""
        self.logger = logging.getLogger("FinanceDataMart")
        self.logger.setLevel(logging.INFO)
        
        # 중복 핸들러 방지
        if not self.logger.handlers:
            # Console Handler
            c_handler = logging.StreamHandler()
            c_handler.setLevel(logging.INFO)
            c_format = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
            c_handler.setFormatter(c_format)
            self.logger.addHandler(c_handler)
            
            # File Handler (error_log.txt)
            f_handler = logging.FileHandler(self.error_log_path, encoding='utf-8')
            f_handler.setLevel(logging.WARNING)
            f_format = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
            f_handler.setFormatter(f_format)
            self.logger.addHandler(f_handler)

    def _init_csv_logs(self):
        """CSV 로그 파일들의 헤더를 초기화합니다."""
        # 1. refresh_log.csv
        if not self.refresh_log_path.exists():
            with open(self.refresh_log_path, mode='w', newline='', encoding='utf-8-sig') as f:
                writer = csv.writer(f)
                writer.writerow([
                    "run_id", "run_datetime", "data_group", 
                    "source_file", "status", "row_count", 
                    "output_file", "message"
                ])
                
        # 2. validation_log.csv
        if not self.validation_log_path.exists():
            with open(self.validation_log_path, mode='w', newline='', encoding='utf-8-sig') as f:
                writer = csv.writer(f)
                writer.writerow(["run_datetime", "step", "status", "message"])

    def _sanitize_message(self, value) -> str:
        """Remove local absolute paths from user-facing log messages."""
        text = "" if value is None else str(value)
        replacements = [
            str(Path.cwd()),
            str(Path.cwd()).replace("\\", "/"),
            str(Path.home()),
            str(Path.home()).replace("\\", "/"),
        ]
        for path_text in replacements:
            if path_text:
                text = text.replace(path_text, "[local_path]")
        return re.sub(r"[A-Za-z]:[\\/][^\s,\")']+", "[local_path]", text)

    def info(self, msg: str):
        self.logger.info(self._sanitize_message(msg))

    def warning(self, msg: str):
        self.logger.warning(self._sanitize_message(msg))

    def error(self, msg: str, err: Exception = None):
        self.logger.error(self._sanitize_message(msg))
        if err:
            with open(self.error_log_path, mode='a', encoding='utf-8') as f:
                f.write(f"\n--- Exception Details at {datetime.now().isoformat()} ---\n")
                f.write(f"{type(err).__name__}: {self._sanitize_message(err)}\n")

    def log_refresh(self, run_id: str, data_group: str, source_file: str, status: str, row_count: int, output_file: str, message: str):
        """refresh_log.csv에 로깅을 추가합니다."""
        run_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            message = self._sanitize_message(message)
            with open(self.refresh_log_path, mode='a', newline='', encoding='utf-8-sig') as f:
                writer = csv.writer(f)
                writer.writerow([
                    run_id, run_datetime, data_group, 
                    source_file, status, row_count, 
                    output_file, message
                ])
        except Exception as e:
            self.logger.error(f"refresh_log.csv 기록 중 오류: {e}")

    def log_validation(self, step: str, status: str, message: str):
        """validation_log.csv에 로깅을 추가합니다."""
        run_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            message = self._sanitize_message(message)
            with open(self.validation_log_path, mode='a', newline='', encoding='utf-8-sig') as f:
                writer = csv.writer(f)
                writer.writerow([run_datetime, step, status, message])
        except Exception as e:
            self.logger.error(f"validation_log.csv 기록 중 오류: {e}")
