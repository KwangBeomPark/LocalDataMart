from pathlib import Path
from typing import Dict, List

import pandas as pd


class ReportGenerator:
    def __init__(self, output_dir: str = "sample_workspace/04_Report_View"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def parse_group_by(self, group_by_str: str) -> List[str]:
        if pd.isna(group_by_str) or not group_by_str:
            return []
        return [col.strip() for col in str(group_by_str).split(",") if col.strip()]

    def parse_measures(self, measures_str: str) -> Dict[str, str]:
        agg_dict = {}
        if pd.isna(measures_str) or not measures_str:
            return agg_dict

        allowed_aggs = {"sum", "count"}
        parts = [p.strip() for p in str(measures_str).split(",") if p.strip()]

        for part in parts:
            if ":" not in part:
                raise ValueError(
                    f"Invalid measure format '{part}' in Report_View config. "
                    f"Must be written as 'column_name:aggregation_function' (e.g., 'net_sales:sum')."
                )

            col, agg = part.split(":", 1)
            col = col.strip()
            agg = agg.strip().lower()

            if not col:
                raise ValueError(f"Measure column name cannot be empty in '{part}'.")
            if not agg:
                raise ValueError(f"Aggregation function cannot be empty in '{part}'.")
            if agg not in allowed_aggs:
                raise ValueError(
                    f"Unsupported aggregation function '{agg}' in '{part}'. "
                    f"Supported functions are: {sorted(list(allowed_aggs))} (e.g., 'net_sales:sum')."
                )

            agg_dict[col] = agg

        return agg_dict

    def validate_report_config(self, view_row: pd.Series, clean_tables: Dict[str, pd.DataFrame]):
        """Report_View 설정 행이 올바른지 사전 검증합니다.

        Args:
            view_row (pd.Series): Report_View 시트의 한 행
            clean_tables (Dict[str, pd.DataFrame]): 현재 생성 완료된 Clean Table 맵

        Raises:
            ValueError, KeyError: 유효성 검증 실패 시
        """
        view_name = view_row["view_name"]
        source_table = view_row["source_table"]
        output_file = str(view_row["output_file"]).strip()

        if Path(output_file).name != output_file or not output_file.lower().endswith(".csv"):
            raise ValueError(
                f"Invalid output_file '{output_file}' for view '{view_name}'. "
                "Report output must be a CSV filename without folder path."
            )

        # 1. source_table 존재 여부 검증 (대소문자 및 _clean 형태 대조)
        matched_key = None
        for group_name in clean_tables.keys():
            if f"{group_name.lower()}_clean" == source_table:
                matched_key = group_name
                break

        if matched_key is None:
            available_tables = [f"{k.lower()}_clean" for k in clean_tables.keys()]
            raise ValueError(
                f"Source table '{source_table}' defined for view '{view_name}' "
                f"does not exist in the generated Clean Tables. "
                f"Available tables: {available_tables}"
            )

        clean_df = clean_tables[matched_key]
        group_by_cols = self.parse_group_by(view_row["group_by"])

        # 2. group_by 컬럼 존재 검증
        if not group_by_cols:
            raise ValueError(f"No group_by columns defined for view: {view_name}")

        available_cols = list(clean_df.columns)
        missing_cols = [col for col in group_by_cols if col not in clean_df.columns]
        if missing_cols:
            raise KeyError(
                f"Group_by column(s) {missing_cols} not found "
                f"in Clean Table '{source_table}' for view '{view_name}'. "
                f"Available columns: {available_cols}"
            )

        # 3. measures 파싱 및 컬럼/함수 검증
        measures_dict = self.parse_measures(view_row["measures"])
        if not measures_dict:
            raise ValueError(f"No measures defined for view: {view_name}")

        missing_measures = [col for col in measures_dict.keys() if col not in clean_df.columns]
        if missing_measures:
            raise KeyError(
                f"Measure column(s) {missing_measures} not found "
                f"in Clean Table '{source_table}' for view '{view_name}'. "
                f"Available columns: {available_cols}"
            )

    def generate_view(self, clean_df: pd.DataFrame, view_row: pd.Series) -> pd.DataFrame:
        view_name = view_row["view_name"]
        source_table = view_row["source_table"]
        group_by_cols = self.parse_group_by(view_row["group_by"])
        measures_dict = self.parse_measures(view_row["measures"])

        if not group_by_cols:
            raise ValueError(f"No group_by columns defined for view: {view_name}")
        if not measures_dict:
            raise ValueError(f"No measures defined for view: {view_name}")

        available_cols = list(clean_df.columns)
        missing_cols = [col for col in group_by_cols if col not in clean_df.columns]
        if missing_cols:
            raise KeyError(
                f"Report_View column validation failed: Group_by column(s) {missing_cols} not found "
                f"in Clean Table '{source_table}' for view '{view_name}'. "
                f"Available columns are: {available_cols}"
            )

        missing_measures = [col for col in measures_dict.keys() if col not in clean_df.columns]
        if missing_measures:
            raise KeyError(
                f"Report_View column validation failed: Measure column(s) {missing_measures} not found "
                f"in Clean Table '{source_table}' for view '{view_name}'. "
                f"Available columns are: {available_cols}"
            )

        return clean_df.groupby(group_by_cols, as_index=False).agg(measures_dict)

    def save_report(self, df: pd.DataFrame, filename: str) -> Path:
        if Path(filename).name != filename or not str(filename).lower().endswith(".csv"):
            raise ValueError("Report output filename must be a CSV filename without folder path.")
        output_path = self.output_dir / filename
        df.to_csv(output_path, index=False, encoding="utf-8-sig")
        return output_path
