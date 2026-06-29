import sys
from pathlib import Path

# 프로젝트 루트를 파이썬 경로에 추가
sys.path.append(str(Path(__file__).resolve().parent.parent))

from app.column_inventory import ColumnInventoryGenerator

def main():
    print("=== Column Inventory Generation Start ===")
    try:
        generator = ColumnInventoryGenerator(
            config_path="sample_workspace/90_Config/config.xlsx",
            output_path="sample_workspace/90_Config/column_inventory.xlsx"
        )
        generator.generate()
        print("=== Column Inventory Generation Finished Successfully ===")
    except Exception as e:
        print(f"Error during column inventory generation: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
