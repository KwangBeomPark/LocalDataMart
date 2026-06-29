from pathlib import Path
import pandas as pd
from typing import Dict, Tuple

class ConfigLoader:
    REQUIRED_SHEETS = ["Source_Config", "Column_Mapping", "Report_View"]
    
    REQUIRED_COLUMNS = {
        "Source_Config": ["active", "data_group", "folder_path", "file_pattern", "sheet_name", "header_row", "period_source", "load_mode"],
        "Column_Mapping": ["data_group", "keep", "raw_column", "standard_column", "role", "data_type", "required", "aggregation"],
        "Report_View": ["active", "view_name", "source_table", "group_by", "measures", "filter", "output_file"]
    }
    
    def __init__(self, config_path: str = "sample_workspace/90_Config/config.xlsx"):
        self.config_path = Path(config_path)

    def validate_file_exists(self):
        """설정 파일이 존재하는지 검증합니다."""
        if not self.config_path.exists():
            raise FileNotFoundError(f"Config file not found at: {self.config_path}")

    def load_all_configs(self) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        """config.xlsx의 모든 설정을 읽어 세 개의 DataFrame으로 반환합니다.
        
        Returns:
            Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]: 
                (Source_Config, Column_Mapping, Report_View) DataFrame 리스트
        """
        self.validate_file_exists()
        
        # openpyxl을 통해 시트 목록 검증
        try:
            with pd.ExcelFile(self.config_path, engine="openpyxl") as excel_file:
                sheet_names = excel_file.sheet_names
        except Exception as e:
            raise ValueError(f"Failed to open config Excel file: {e}")
            
        for sheet in self.REQUIRED_SHEETS:
            if sheet not in sheet_names:
                raise ValueError(f"Required sheet '{sheet}' is missing from config.xlsx")

        # 각 시트 로드
        df_source = pd.read_excel(self.config_path, sheet_name="Source_Config", engine="openpyxl")
        df_mapping = pd.read_excel(self.config_path, sheet_name="Column_Mapping", engine="openpyxl")
        df_report = pd.read_excel(self.config_path, sheet_name="Report_View", engine="openpyxl")
        
        # 각 시트 필수 컬럼 유무 검증
        for sheet_name, required_cols in self.REQUIRED_COLUMNS.items():
            if sheet_name == "Source_Config":
                df_target = df_source
            elif sheet_name == "Column_Mapping":
                df_target = df_mapping
            else:
                df_target = df_report
                
            missing_cols = [col for col in required_cols if col not in df_target.columns]
            if missing_cols:
                raise ValueError(f"Required column(s) {missing_cols} is/are missing in config sheet '{sheet_name}'")

        # 문자열 컬럼들의 앞뒤 공백 제거 및 문자열화
        for df in [df_source, df_mapping, df_report]:
            for col in df.select_dtypes(include=['object']).columns:
                df[col] = df[col].astype(str).str.strip()

        # 주요 플래그 컬럼 대문자 변환 및 Y/N 무결성 검증
        for sheet_name, df, flag_cols in [
            ("Source_Config", df_source, ["active"]),
            ("Column_Mapping", df_mapping, ["keep", "required"]),
            ("Report_View", df_report, ["active"]),
        ]:
            for col in flag_cols:
                if col in df.columns:
                    # 빈값이 유입된 경우를 고려하여 처리
                    df[col] = df[col].astype(str).str.strip().str.upper()
                    # 결측치("NAN", "NONE" 등)가 유입되었거나 Y/N가 아닌 값 검출
                    invalid_mask = ~df[col].isin(["Y", "N"])
                    if invalid_mask.any():
                        invalid_rows = df[invalid_mask]
                        first_err_idx = invalid_rows.index[0] + 1  # 1-based index
                        wrong_val = invalid_rows.iloc[0][col]
                        raise ValueError(
                            f"Configuration validation failed: In sheet '{sheet_name}', column '{col}' "
                            f"contains an invalid value '{wrong_val}' at row {first_err_idx}. "
                            f"Only 'Y' or 'N' (case-insensitive) are allowed."
                        )
                
        return df_source, df_mapping, df_report
