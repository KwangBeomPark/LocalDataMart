import os
import sys
import shutil
import subprocess
from pathlib import Path

def clean_build_folders(project_root: Path):
    """이전 빌드 부산물을 클린업하여 컴파일 충돌을 예방합니다."""
    print("Cleaning legacy build directories...")
    folders = [project_root / "build", project_root / "dist"]
    for folder in folders:
        if folder.exists():
            try:
                shutil.rmtree(folder)
                print(f" - Cleaned folder: {folder.name}")
            except Exception as e:
                print(f" - Warning: Failed to clean {folder.name}: {e}")

def main():
    print("=========================================================")
    print("   Finance DataMart - Standalone & Setup Builder         ")
    print("=========================================================")

    project_root = Path(__file__).resolve().parent.parent
    clean_build_folders(project_root)

    # --- 0단계: 빌드 타임에 sample_workspace 엑셀 템플릿 재생성 ---
    print("Generating clean sample workspace for packaging...")
    subprocess.run([sys.executable, "scripts/create_sample_data.py"], check=True, cwd=project_root)

    # --- 1단계: FinanceDataMart.exe (실제 GUI 앱) 컴파일 ---
    print("\n[Phase 1/2] Compiling GUI application (FinanceDataMart.exe)...")
    gui_entry = project_root / "scripts" / "run_desktop_app.py"
    
    gui_cmd = [
        "pyinstaller",
        "--onefile",
        "--noconsole",
        "--name", "FinanceDataMart",
        str(gui_entry)
    ]
    
    print("Command:", " ".join(gui_cmd))
    subprocess.run(gui_cmd, check=True, cwd=project_root)
    
    compiled_app = project_root / "dist" / "FinanceDataMart.exe"
    if not compiled_app.exists():
        print("ERROR: GUI application compilation failed. File not found.")
        sys.exit(1)
    print("SUCCESS: FinanceDataMart.exe generated.")

    # --- 2단계: FinanceDataMart_Setup.exe (인스톨러) 컴파일 ---
    print("\n[Phase 2/2] Compiling Setup Installer (FinanceDataMart_Setup.exe)...")
    setup_entry = project_root / "scripts" / "setup_installer.py"
    
    # 임베딩할 자산 목록 (FinanceDataMart.exe를 포함하여 전체 36종 소스/문서 바인딩)
    add_data_targets = [
        ("dist/FinanceDataMart.exe", "."),  # 1단계의 컴파일 결과물
        ("app", "app"),
        ("scripts", "scripts"),
        ("requirements.txt", "."),
        ("README.md", "."),
        ("LICENSE", "."),
        ("AI_CODE_MAP.MD", "."),
        ("PROJECT_ROADMAP.MD", "."),
        ("myAGENT.MD", "."),
        ("USER_GUIDE.md", "."),
        ("KNOWN_LIMITATIONS.md", "."),
        ("PUBLIC_RELEASE_CHECKLIST.md", "."),
        ("RELEASE_NOTES.md", "."),
        ("THIRD_PARTY_NOTICES.md", "."),
        ("GITHUB_RELEASE_GUIDE.md", "."),
        ("MAINTENANCE.md", "."),
        ("RELEASE_MANIFEST.md", "."),
        ("OFFICIAL_RELEASE_HANDOFF.md", "."),
        ("POST_RELEASE_CHECKLIST.md", "."),
        ("LICENSE_DECISION_GUIDE.md", "."),
        ("DISTRIBUTION_TEST_GUIDE.md", "."),
        (".gitignore", "."),
        ("sample_workspace", "sample_workspace"),
    ]

    setup_cmd = [
        "pyinstaller",
        "--onefile",
        "--console",
        "--name", "FinanceDataMart_Setup",
    ]

    for src, dest in add_data_targets:
        src_path = project_root / src
        param = f"{str(src_path)}{os.pathsep}{dest}"
        setup_cmd.extend(["--add-data", param])
        
    setup_cmd.append(str(setup_entry))
    
    print("Command:", " ".join(setup_cmd))
    subprocess.run(setup_cmd, check=True, cwd=project_root)

    compiled_setup = project_root / "dist" / "FinanceDataMart_Setup.exe"
    if not compiled_setup.exists():
        print("ERROR: Setup installer compilation failed. File not found.")
        sys.exit(1)
        
    print("\n---------------------------------------------------------")
    print("SUCCESS: Standalone Setup installer generated successfully!")
    print(f"   Target Setup File: {compiled_setup}")
    print("=========================================================")

if __name__ == "__main__":
    main()
