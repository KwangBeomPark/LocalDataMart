import pandas as pd
from pathlib import Path

from app.config_loader import ConfigLoader
from app.file_scanner import FileScanner
from app.excel_reader import ExcelReader

class ColumnInventoryGenerator:
    def __init__(self, 
                 config_path: str = "sample_workspace/90_Config/config.xlsx",
                 output_path: str = "sample_workspace/90_Config/column_inventory.xlsx"):
        self.config_path = Path(config_path)
        self.output_path = Path(output_path)

    def infer_column_type(self, series: pd.Series) -> str:
        """Pandas Series의 값을 기준으로 데이터 타입을 추론합니다."""
        valid_series = series.dropna()
        if valid_series.empty:
            return "unknown"

        # 1. Datetime 계열 감지
        if pd.api.types.is_datetime64_any_dtype(series):
            return "date"

        # 2. 수치형(정수, 실수) 감지
        if pd.api.types.is_numeric_dtype(series):
            # boolean 판별
            if pd.api.types.is_bool_dtype(series):
                return "text"
            return "number"

        # 3. 날짜형 텍스트 감지 시도
        try:
            sample_vals = valid_series.iloc[:3].astype(str).str.strip()
            date_like = any(
                pd.Series(sample_vals).str.contains(r"\d{4}[-/.]\d{2}[-/.]\d{2}|\d{8}")
            )
            if date_like:
                parsed = pd.to_datetime(sample_vals, errors="coerce")
                if not parsed.isna().any():
                    return "date"
        except Exception:
            pass

        # 4. 기본값은 text로 취급
        return "text"

    def collect_sample_values(self, series: pd.Series, max_samples: int = 3) -> str:
        """중복이 없는 고유 값 중 상위 N개를 쉼표로 연결해 반환합니다."""
        valid_series = series.dropna()
        if valid_series.empty:
            return ""
        
        # 고유값 추출 (순서 보존을 위해 unique() 사용)
        unique_vals = valid_series.unique()
        samples = [str(val).strip() for val in unique_vals[:max_samples]]
        return ", ".join(samples)

    def generate(self):
        """Source_Config의 모든 활성 데이터 그룹 경로를 스캔하고 column_inventory.xlsx를 생성합니다."""
        print(f"Loading config from: {self.config_path}")
        config_loader = ConfigLoader(config_path=str(self.config_path))
        df_source, _, _ = config_loader.load_all_configs()

        active_sources = df_source[df_source["active"] == "Y"]
        if active_sources.empty:
            print("No active source configurations found.")
            return

        inventory_records = []

        for _, source_row in active_sources.iterrows():
            data_group = source_row["data_group"]
            folder_path = source_row["folder_path"]
            file_pattern = source_row["file_pattern"]
            sheet_name = source_row["sheet_name"]
            header_row = int(source_row["header_row"])

            print(f"Scanning data group '{data_group}' at '{folder_path}'...")
            
            try:
                files = FileScanner.scan_files(folder_path, file_pattern)
            except Exception as e:
                print(f"Error scanning folder '{folder_path}': {e}")
                continue

            if not files:
                print(f"No files found for group '{data_group}' matching pattern '{file_pattern}'")
                continue

            # 파일별 스캔 (최초 1~2개 대표 파일 혹은 전체 파일)
            # MVP의 Column Inventory 스캔 편의를 위해 발견된 모든 파일의 모든 컬럼을 전개
            for file_path in files:
                print(f"Analyzing columns in file: {file_path.name}")
                try:
                    df = ExcelReader.read_sheet(file_path, sheet_name, header_row)
                except Exception as e:
                    print(f"Error reading file '{file_path.name}': {e}")
                    continue

                total_rows = len(df)
                
                for col in df.columns:
                    series = df[col]
                    
                    non_null_count = int(series.notna().sum())
                    null_count = int(series.isna().sum())
                    null_ratio = float(null_count / total_rows) if total_rows > 0 else 0.0
                    
                    inferred_type = self.infer_column_type(series)
                    sample_vals = self.collect_sample_values(series, max_samples=3)
                    
                    inventory_records.append({
                        "data_group": data_group,
                        "source_file": file_path.name,
                        "sheet_name": sheet_name,
                        "raw_column": str(col).strip(),
                        "inferred_type": inferred_type,
                        "sample_values": sample_vals,
                        "non_null_count": non_null_count,
                        "null_count": null_count,
                        "null_ratio": round(null_ratio, 4),
                        "keep_candidate": "N",
                        "memo": ""
                    })

        if not inventory_records:
            print("No column metadata could be extracted.")
            return

        # 결과 DataFrame 생성 및 저장
        df_inventory = pd.DataFrame(inventory_records)
        
        self.output_path.parent.mkdir(parents=True, exist_ok=True)
        try:
            df_inventory.to_excel(self.output_path, sheet_name="Column_Inventory", index=False)
            print(f"Successfully generated column inventory at: {self.output_path}")
        except Exception as e:
            print(f"Failed to save column inventory Excel: {e}")
            raise e
