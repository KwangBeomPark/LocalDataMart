import os
import sys
import shutil
import subprocess
from pathlib import Path
import re

# 프로젝트 루트를 임포트 패스에 추가 (로컬 빌드/실행 대비)
sys.path.append(str(Path(__file__).resolve().parent.parent))

def get_bundle_dir():
    """PyInstaller 런타임 임시 해제 디렉토리 또는 로컬 개발 환경 경로를 가져옵니다."""
    if getattr(sys, 'frozen', False):
        return Path(sys._MEIPASS)
    return Path(__file__).resolve().parent.parent


def sanitize_message(value) -> str:
    text = "" if value is None else str(value)
    replacements = [
        str(Path.home()),
        str(Path.home()).replace("\\", "/"),
    ]
    for path_text in replacements:
        if path_text:
            text = text.replace(path_text, "[user_home]")
    return re.sub(r"[A-Za-z]:[\\/][^\s,\")']+", "[local_path]", text)

def copy_standalone_files(src_dir: Path, dest_dir: Path):
    """임베딩된 standalone GUI 파일 및 문서 자산을 AppData 디렉토리로 안전 복사합니다."""
    print("Step 1: Copying standalone application files to AppData...")
    dest_dir.mkdir(parents=True, exist_ok=True)
    
    # 복사 대상 목록 정의
    copy_targets = [
        ("FinanceDataMart.exe", False),  # 독립 실행 GUI 바이너리
        ("README.md", False),
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
                shutil.copytree(src_path, dest_path)
                print(f" - Directory copied: {name}")
            else:
                shutil.copy2(src_path, dest_path)
                print(f" - File copied: {name}")
        else:
            # 빌드 타임에 add-data로 바인딩되므로 런타임엔 sys._MEIPASS 루트에 존재함
            # 따라서 src_dir에 없을 시 sys._MEIPASS 루트에서 직접 검색/복사 시도
            fallback_path = Path(sys._MEIPASS) / name if getattr(sys, 'frozen', False) else src_path
            if fallback_path.exists():
                shutil.copy2(fallback_path, dest_path)
                print(f" - File copied (fallback): {name}")
            else:
                print(f" - Warning: Target {name} not found in bundle.")

def initialize_sample_data(src_dir: Path, dest_dir: Path):
    """임베딩된 가상 sample_workspace 템플릿 폴더 구조를 통째로 설치 경로에 복원합니다."""
    print("Step 2: Restoring virtual sample workspace and configurations...")
    src_workspace = src_dir / "sample_workspace"
    dest_workspace = dest_dir / "sample_workspace"
    
    if src_workspace.exists():
        if dest_workspace.exists():
            shutil.rmtree(dest_workspace)
        shutil.copytree(src_workspace, dest_workspace)
        print(" - Sample workspace and configurations restored successfully.")
    else:
        fallback_workspace = Path(sys._MEIPASS) / "sample_workspace" if getattr(sys, 'frozen', False) else src_workspace
        if fallback_workspace.exists():
            if dest_workspace.exists():
                shutil.rmtree(dest_workspace)
            shutil.copytree(fallback_workspace, dest_workspace)
            print(" - Sample workspace restored via fallback bundle path.")
        else:
            print(" - Warning: Pre-packaged sample_workspace folder not found.")

def create_desktop_shortcut(dest_dir: Path):
    """사용자 바탕화면(Desktop)에 GUI 앱 바로가기 아이콘을 생성합니다."""
    print("Step 3: Creating desktop shortcut pointing to Standalone EXE...")
    
    app_exe = dest_dir / "FinanceDataMart.exe"
    
    # PowerShell 스크립트를 사용하여 OneDrive 바탕화면 및 다국어 지원 대응 바로가기 생성
    # TargetPath는 독립 실행 파일인 FinanceDataMart.exe를 직접 지목합니다.
    ps_cmd = (
        f"$DesktopPath = [Environment]::GetFolderPath('Desktop'); "
        f"$WshShell = New-Object -ComObject WScript.Shell; "
        f"$Shortcut = $WshShell.CreateShortcut(\"$DesktopPath\\FinanceDataMart.lnk\"); "
        f"$Shortcut.TargetPath = '{str(app_exe)}'; "
        f"$Shortcut.WorkingDirectory = '{str(dest_dir)}'; "
        f"$Shortcut.Description = 'Finance DataMart Tool (Standalone)'; "
        f"$Shortcut.Save()"
    )
    
    subprocess.run(["powershell", "-Command", ps_cmd], check=True)
    print(" - Desktop shortcut successfully created.")

def main():
    print("=========================================================")
    print("   Finance DataMart - Standalone AppData Setup           ")
    print("=========================================================")
    
    appdata_local = Path(os.environ["LOCALAPPDATA"])
    dest_dir = appdata_local / "FinanceDataMart"
    src_dir = get_bundle_dir()
    
    print("Target Installation Directory: %LOCALAPPDATA%\\FinanceDataMart")
    print("---------------------------------------------------------")
    
    try:
        # 1. 파일 복사
        copy_standalone_files(src_dir, dest_dir)
        
        # 2. 샘플 템플릿 복구 (natively 구동)
        initialize_sample_data(src_dir, dest_dir)
        
        # 3. 바로가기 연결
        create_desktop_shortcut(dest_dir)
        
        print("---------------------------------------------------------")
        print("SUCCESS: Standalone installation completed successfully!")
        print("   You can now run the app via the desktop shortcut: 'FinanceDataMart'")
        print("=========================================================")
        
    except Exception as e:
        print("\nERROR: Setup failed due to the following error:")
        print(f"Error details: {sanitize_message(e)}")
        print("=========================================================")
        sys.exit(1)

if __name__ == "__main__":
    main()
