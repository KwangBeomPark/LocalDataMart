import sys
from pathlib import Path

# 프로젝트 루트를 파이썬 경로에 추가
sys.path.append(str(Path(__file__).resolve().parent.parent))

from app.ui_app import launch

def main():
    print("Launching Desktop UI App...")
    launch()

if __name__ == "__main__":
    main()
