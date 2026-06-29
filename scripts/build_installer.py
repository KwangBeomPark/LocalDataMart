import os
import sys
import subprocess
from pathlib import Path

def main():
    print("=========================================================")
    print("   Finance DataMart Installer - PyInstaller Builder      ")
    print("=========================================================")

    project_root = Path(__file__).resolve().parent.parent
    installer_script = project_root / "scripts" / "installer.py"
    
    # 배포 34종 자산을 PyInstaller 리소스 패킹용 파라미터로 매핑
    add_data_targets = [
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
    ]
    
    pyinstaller_cmd = [
        "pyinstaller",
        "--onefile",
        "--name", "FinanceDataMart_Installer",
        "--console", 
    ]
    
    for src, dest in add_data_targets:
        src_path = project_root / src
        param = f"{str(src_path)}{os.pathsep}{dest}"
        pyinstaller_cmd.extend(["--add-data", param])
        
    pyinstaller_cmd.append(str(installer_script))
    
    print("Starting PyInstaller compilation command:")
    print(" ".join(pyinstaller_cmd))
    print("---------------------------------------------------------")
    
    try:
        # PyInstaller 구동
        result = subprocess.run(pyinstaller_cmd, check=True, cwd=project_root)
        if result.returncode == 0:
            print("---------------------------------------------------------")
            print("SUCCESS: Installer executable successfully generated!")
            print(f"   Target executable: {project_root / 'dist' / 'FinanceDataMart_Installer.exe'}")
            print("=========================================================")
        else:
            print("ERROR: Builder finished with non-zero return code.")
            sys.exit(1)
            
    except Exception as e:
        print(f"ERROR: Builder execution failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
