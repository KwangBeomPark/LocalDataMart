from pathlib import Path
import pandas as pd

class ExcelReader:
    @staticmethod
    def read_sheet(file_path: Path, sheet_name: str, header_row: int) -> pd.DataFrame:
        """엑셀 파일에서 지정된 시트와 헤더 위치를 사용하여 데이터를 DataFrame으로 읽습니다.
        
        Args:
            file_path (Path): 읽을 엑셀 파일 경로
            sheet_name (str): 엑셀 시트 이름
            header_row (int): 헤더 행 번호 (1-based index)
            
        Returns:
            pd.DataFrame: 로드된 DataFrame
        """
        # pandas read_excel의 header 파라미터는 0-based index
        header_index = int(header_row) - 1 if header_row > 0 else 0
        
        try:
            df = pd.read_excel(
                file_path, 
                sheet_name=sheet_name, 
                header=header_index, 
                engine="openpyxl"
            )
            return df
        except Exception as e:
            raise ValueError(f"Failed to read sheet '{sheet_name}' from {file_path.name}: {e}")
