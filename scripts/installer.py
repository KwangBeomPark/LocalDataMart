import os
import sys
import shutil
import subprocess
from pathlib import Path

def find_system_python():
    """Return a system Python command usable for creating a venv."""
    candidates = [
        ["py", "-3"],
        ["python"],
        ["python3"],
    ]
    for cmd in candidates:
        executable = shutil.which(cmd[0])
        if not executable:
            continue
        try:
            subprocess.run(
                cmd + ["--version"],
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            return cmd
        except Exception:
            continue
    raise RuntimeError(
        "Python 3 was not found on PATH. Install Python 3.8+ and enable PATH, then rerun this installer."
    )

def get_bundle_dir():
    """PyInstaller 런타임 임시 풀림 경로 또는 로컬 스크립트 실행 경로를 반환합니다."""
    if getattr(sys, 'frozen', False):
        return Path(sys._MEIPASS)
    return Path(__file__).resolve().parent.parent

def copy_distribution_files(src_dir: Path, dest_dir: Path):
    """지정된 소스 디렉토리에서 목적지 AppData 디렉토리로 배포 자산을 복사합니다."""
    print("Step 1: Copying distribution files to AppData...")
    dest_dir.mkdir(parents=True, exist_ok=True)

    # 복사할 핵심 대상 정의
    copy_targets = [
        ("app", True),
        ("scripts", True),
        ("README.md", False),
        ("requirements.txt", False),
        ("LICENSE", False),
        ("AI_CODE_MAP.MD", False),
        ("PROJECT_ROADMAP.MD", False),
        ("myAGENT.MD", False),
        ("USER_GUIDE.md", False),
        ("KNOWN_LIMITATIONS.md", False),
        ("PUBLIC_RELEASE_CHECKLIST.md", False),
        ("RELEASE_NOTES.md", False),
        ("THIRD_PARTY_NOTICES.md", False),
        ("GITHUB_RELEASE_GUIDE.md", False),
        ("MAINTENANCE.md", False),
        ("RELEASE_MANIFEST.md", False),
        ("OFFICIAL_RELEASE_HANDOFF.md", False),
        ("POST_RELEASE_CHECKLIST.md", False),
        ("LICENSE_DECISION_GUIDE.md", False),
        ("DISTRIBUTION_TEST_GUIDE.md", False),
        (".gitignore", False),
    ]

    for name, is_dir in copy_targets:
        src_path = src_dir / name
        dest_path = dest_dir / name
        if src_path.exists():
            if is_dir:
                if dest_path.exists():
                    shutil.rmtree(dest_path)
                # 캐시 (__pycache__) 복사 제외
                shutil.copytree(src_path, dest_path, ignore=shutil.ignore_patterns("__pycache__", "*.pyc", "*.pyo"))
                print(f" - Directory copied: {name}")
            else:
                shutil.copy2(src_path, dest_path)
                print(f" - File copied: {name}")
        else:
            print(f" - Warning: Target {name} not found in source.")

def setup_virtual_environment(dest_dir: Path):
    """AppData 설치 경로 내에 파이썬 가상환경을 구성하고 라이브러리를 설치합니다."""
    print("Step 2: Configuring Python virtual environment (.venv)...")
    venv_dir = dest_dir / ".venv"
    python_cmd = find_system_python()

    if not venv_dir.exists():
        subprocess.run(python_cmd + ["-m", "venv", str(venv_dir)], check=True, cwd=dest_dir)
        print(" - Virtual environment (.venv) created successfully.")
    else:
        print(" - Virtual environment (.venv) already exists. Skipping creation.")

    # pip 의존성 라이브러리 설치
    print("Step 3: Installing external dependencies via pip...")
    pip_exe = venv_dir / "Scripts" / "pip.exe"
    if not pip_exe.exists():
        pip_exe = venv_dir / "Scripts" / "pip"

    subprocess.run([str(pip_exe), "install", "-r", "requirements.txt"], check=True, cwd=dest_dir)
    print(" - External packages (pandas, openpyxl) installed successfully.")

def initialize_sample_data(dest_dir: Path):
    """가상 샘플 데이터 및 config 엑셀 설정을 자동으로 생성합니다."""
    print("Step 4: Initializing virtual sample data and configuration...")
    venv_python = dest_dir / ".venv" / "Scripts" / "python.exe"
    if not venv_python.exists():
        venv_python = dest_dir / ".venv" / "Scripts" / "python"

    subprocess.run([str(venv_python), "scripts/create_sample_data.py"], check=True, cwd=dest_dir)
    print(" - Virtual sample workspace and config.xlsx created successfully.")

def create_desktop_shortcut(dest_dir: Path):
    """사용자 바탕화면(Desktop)에 GUI 앱 바로가기 아이콘을 생성합니다."""
    print("Step 5: Creating desktop shortcut for GUI application...")

    venv_pythonw = dest_dir / ".venv" / "Scripts" / "pythonw.exe"
    app_script = dest_dir / "scripts" / "run_desktop_app.py"

    # PowerShell 문자열에서 홑따옴표가 오동작하지 않도록 이스케이프 처리
    venv_pythonw_str = str(venv_pythonw).replace("'", "''")
    app_script_str = str(app_script).replace("'", "''")
    dest_dir_str = str(dest_dir).replace("'", "''")

    # PowerShell 스크립트를 사용하여 OneDrive 바탕화면 및 다국어 지원 대응 바로가기 생성
    ps_cmd = (
        f"$DesktopPath = [Environment]::GetFolderPath('Desktop'); "
        f"if (-not $DesktopPath) {{ $DesktopPath = [System.IO.Path]::Combine($env:USERPROFILE, 'Desktop') }}; "
        f"$WshShell = New-Object -ComObject WScript.Shell; "
        f"$Shortcut = $WshShell.CreateShortcut(\"$DesktopPath\\FinanceDataMart.lnk\"); "
        f"$Shortcut.TargetPath = '{venv_pythonw_str}'; "
        f"$Shortcut.Arguments = '\"{app_script_str}\"'; "
        f"$Shortcut.WorkingDirectory = '{dest_dir_str}'; "
        f"$Shortcut.Description = 'Finance DataMart Tool GUI App'; "
        f"$Shortcut.Save()"
    )

    subprocess.run(["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", ps_cmd], check=True)
    print(" - Desktop shortcut successfully created.")

def main():
    print("=========================================================")
    print("   Finance DataMart Tool - AppData Local Installer       ")
    print("=========================================================")
    print("[Notice] This installer does not require Administrator privileges.")
    print("         If Windows SmartScreen warns you, click 'More info' ")
    print("         and then 'Run anyway' to proceed.")
    print("=========================================================")

    # AppData 설치 경로 설정
    appdata_local = Path(os.environ["LOCALAPPDATA"])
    dest_dir = appdata_local / "FinanceDataMart"
    src_dir = get_bundle_dir()

    print(f"Target Installation Directory: {dest_dir}")
    print(f"Source Resource Directory    : {src_dir}")
    print("---------------------------------------------------------")

    try:
        # 1. 파일 복사
        copy_distribution_files(src_dir, dest_dir)

        # 2. 가상환경 생성
        setup_virtual_environment(dest_dir)

        # 3. 샘플 생성 스크립트 가동
        initialize_sample_data(dest_dir)

        # 4. 바로가기 생성
        create_desktop_shortcut(dest_dir)

        print("---------------------------------------------------------")
        print("SUCCESS: Installation completed successfully!")
        print("   You can now launch the application via the desktop shortcut: 'FinanceDataMart'")
        print("=========================================================")
        input("\nPress Enter to exit...")

    except PermissionError as pe:
        print("\nERROR: Access Denied (PermissionError).")
        print("The application files or configurations might be locked by another process.")
        print("Please ensure that:")
        print(" 1. The application (FinanceDataMart) or command processes are NOT currently running.")
        print(" 2. None of the files in the target directory (especially config.xlsx or result CSV files) are open in Excel.")
        print("Please close any running instances or open files and try again.")
        print("=========================================================")
        input("\nPress Enter to exit...")
        sys.exit(1)

    except Exception as e:
        print("\nERROR: Installation failed due to the following error:")
        print(f"Error details: {e}")
        print("=========================================================")
        input("\nPress Enter to exit...")
        sys.exit(1)

if __name__ == "__main__":
    main()
