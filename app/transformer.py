import re
from pathlib import Path
from datetime import datetime
import pandas as pd
from typing import List, Dict

class Transformer:
    def __init__(self, column_mapping: pd.DataFrame):
        """
        Args:
            column_mapping (pd.DataFrame): config.xlsx에서 읽은 Column_Mapping DataFrame
        """
        self.mapping_df = column_mapping

    def get_group_mappings(self, data_group: str) -> pd.DataFrame:
        """지정한 data_group에 해당하는 매핑 룰만 필터링합니다."""
        return self.mapping_df[
            (self.mapping_df["data_group"] == data_group) & 
            (self.mapping_df["keep"] == "Y")
        ]

    def extract_period_from_filename(self, filename: str) -> str:
        """파일명에서 YYYY-MM 형태의 기간을 추출합니다. (예: Sales_Closing_2026_01.xlsx -> 2026-01)"""
        # YYYY_MM 또는 YYYY-MM 패턴 매칭
        match = re.search(r"(\d{4})[_-](\d{2})", filename)
        if match:
            return f"{match.group(1)}-{match.group(2)}"
        return "UNKNOWN"

    def transform_single_file(self, df: pd.DataFrame, file_path: Path, source_config_row: pd.Series) -> pd.DataFrame:
        """단일 Raw DataFrame에 매핑, 타입 변환 및 audit 컬럼을 적용합니다."""
        data_group = source_config_row["data_group"]
        period_source = source_config_row.get("period_source", "filename")
        
        # 1. 컬럼 매핑 필터
        group_rules = self.get_group_mappings(data_group)
        if group_rules.empty:
            raise ValueError(f"No active column mapping found for data group: {data_group}")

        # 원본 파일에 매핑에 정의된 raw_column이 있는지 검증
        for _, rule in group_rules.iterrows():
            raw_col = rule["raw_column"]
            required = rule["required"]
            if raw_col not in df.columns:
                if required == "Y":
                    raise KeyError(f"Required raw column '{raw_col}' is missing in file: {file_path.name}")
                else:
                    # 필수 컬럼이 아니면 빈값(NaN)으로 컬럼 생성
                    df[raw_col] = pd.NA

        # 2. 필요한 컬럼만 필터링 및 이름 변경
        raw_cols_to_keep = group_rules["raw_column"].tolist()
        rename_dict = dict(zip(group_rules["raw_column"], group_rules["standard_column"]))
        
        df_filtered = df[raw_cols_to_keep].copy()
        df_filtered.rename(columns=rename_dict, inplace=True)

        # 3. 데이터 타입 변환
        for _, rule in group_rules.iterrows():
            std_col = rule["standard_column"]
            d_type = rule["data_type"]
            
            if std_col not in df_filtered.columns:
                continue
                
            if d_type == "number":
                # 숫자형 변환, 오류 발생 시 NaN
                df_filtered[std_col] = pd.to_numeric(df_filtered[std_col], errors="coerce")
            elif d_type == "date":
                # 날짜형 변환, 오류 발생 시 NaT
                df_filtered[std_col] = pd.to_datetime(df_filtered[std_col], errors="coerce")
            elif d_type == "text":
                # 텍스트형 변환
                df_filtered[std_col] = df_filtered[std_col].astype(str).str.strip()
                # 'nan'이나 'None' 문자열 결측 처리
                df_filtered[std_col] = df_filtered[std_col].replace({"nan": None, "None": None})

        # 3.5. 필수 컬럼의 결측치 검증
        for _, rule in group_rules.iterrows():
            std_col = rule["standard_column"]
            required = rule["required"]
            
            if required == "Y" and std_col in df_filtered.columns:
                # 결측치 체크 (isna, None, 빈 문자열 등)
                null_mask = (
                    df_filtered[std_col].isna() | 
                    (df_filtered[std_col] == "") | 
                    (df_filtered[std_col].astype(str).str.strip() == "")
                )
                if null_mask.any():
                    null_count = null_mask.sum()
                    first_null_idx = df_filtered[null_mask].index[0] + 1  # 1-based index
                    raise ValueError(
                        f"Validation error: Required column '{std_col}' contains {null_count} null/empty value(s) "
                        f"in file '{file_path.name}' (first error at data row {first_null_idx})."
                    )

        # 4. 기간(posting_month) 파생 컬럼 생성
        if period_source == "filename":
            period_val = self.extract_period_from_filename(file_path.name)
            df_filtered["posting_month"] = period_val
        else:
            # 데이터 내의 첫 번째 date 타입 컬럼(기본적으로 posting_date) 기준으로 생성
            date_rules = group_rules[group_rules["data_type"] == "date"]
            if not date_rules.empty:
                date_col = date_rules.iloc[0]["standard_column"]
                df_filtered["posting_month"] = pd.to_datetime(df_filtered[date_col]).dt.strftime("%Y-%m")
            else:
                df_filtered["posting_month"] = "UNKNOWN"

        # 5. Audit 컬럼 추가
        df_filtered["source_file"] = file_path.name
        df_filtered["loaded_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        return df_filtered

    @staticmethod
    def combine_dataframes(dfs: List[pd.DataFrame]) -> pd.DataFrame:
        """변환된 여러 DataFrame을 하나로 병합합니다."""
        if not dfs:
            return pd.DataFrame()
        return pd.concat(dfs, ignore_index=True)
