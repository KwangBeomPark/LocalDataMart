from pathlib import Path
from typing import List

class FileScanner:
    @staticmethod
    def scan_files(folder_path: str, file_pattern: str) -> List[Path]:
        """지정한 폴더 내에서 패턴에 부합하는 파일 목록을 스캔합니다.
        
        Args:
            folder_path (str): 스캔할 폴더 경로
            file_pattern (str): 파일 매칭 패턴 (예: *.xlsx)
            
        Returns:
            List[Path]: 스캔된 파일 경로 리스트 (정렬됨)
        """
        path = Path(folder_path)
        if not path.exists():
            raise FileNotFoundError(f"Source folder does not exist: {path}")
            
        if not path.is_dir():
            raise NotADirectoryError(f"Source path is not a directory: {path}")

        matched_files = list(path.glob(file_pattern))
        
        # 엑셀 임시/잠금 파일(예: ~$Sales_Closing_2026_01.xlsx) 제외
        valid_files = [
            f for f in matched_files 
            if f.is_file() and not f.name.startswith("~$")
        ]
        
        # 파일명 순 정렬
        valid_files.sort(key=lambda x: x.name)
        
        return valid_files
