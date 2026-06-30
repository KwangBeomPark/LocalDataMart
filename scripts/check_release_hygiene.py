import subprocess
import sys
import fnmatch
import os
import re
from pathlib import Path

FORBIDDEN_PATTERNS = [
    'sample_workspace/*',
    'tool/*',
    'build/*',
    'dist/*',
    '.venv/*',
    'venv/*',
    'env/*',
    'ENV/*',
    '__pycache__/*',
    '*/__pycache__/*',
    '.pytest_cache/*',
    '*/.pytest_cache/*',
    '.mypy_cache/*',
    '*/.mypy_cache/*',
    '*.pyc',
    '*.pyo',
    '*.pyd',
    '*.spec',
]

PROJECT_ROOT = Path(__file__).resolve().parent.parent
MANIFEST_PATH = PROJECT_ROOT / "RELEASE_MANIFEST.md"

def check_hygiene():
    print("=== Start Release Hygiene Check ===")
    try:
        # Run git ls-files to get tracked files
        result = subprocess.run(
            ['git', 'ls-files'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        tracked_files = [line.strip().replace('\\', '/') for line in result.stdout.splitlines() if line.strip()]
    except Exception as e:
        print(f"[ERROR] Failed to run 'git ls-files': {e}")
        # If git is not available (e.g. in a non-git environment), we exit with error.
        sys.exit(1)

    violating_files = []
    for file_path in tracked_files:
        # Normalize path separators to forward slashes for cross-platform fnmatch compatibility
        normalized_path = file_path.replace('\\', '/')

        # Check standard forbidden patterns
        matched = False
        for pattern in FORBIDDEN_PATTERNS:
            if fnmatch.fnmatch(normalized_path, pattern) or fnmatch.fnmatch(os.path.basename(normalized_path), pattern):
                violating_files.append((file_path, f"Matches forbidden pattern: {pattern}"))
                matched = True
                break

        if matched:
            continue

        # Extra check: runtime log/output files under 99_Logs
        if "99_Logs/" in normalized_path:
            violating_files.append((file_path, "Runtime log file inside 99_Logs"))

    manifest_errors = []
    if not MANIFEST_PATH.exists():
        manifest_errors.append(("RELEASE_MANIFEST.md", "Manifest file is missing"))
    else:
        manifest_text = MANIFEST_PATH.read_text(encoding="utf-8")
        manifest_files = re.findall(r"^- `([^`]+)`:", manifest_text, flags=re.MULTILINE)
        tracked_set = set(tracked_files)
        for manifest_file in manifest_files:
            normalized_manifest_file = manifest_file.replace('\\', '/')
            if not (PROJECT_ROOT / manifest_file).exists():
                manifest_errors.append((manifest_file, "Manifest file entry does not exist on disk"))
            elif normalized_manifest_file not in tracked_set:
                manifest_errors.append((manifest_file, "Manifest file entry is not tracked by Git"))

    if violating_files or manifest_errors:
        print("[FAIL] Git tracked files contain forbidden release targets!")
        for file, reason in violating_files:
            print(f"  - {file} ({reason})")
        if manifest_errors:
            print("[FAIL] Release manifest contains files that are missing or not tracked by Git!")
            for file, reason in manifest_errors:
                print(f"  - {file} ({reason})")
        sys.exit(1)
    else:
        print("Release hygiene check PASS")
        sys.exit(0)

if __name__ == '__main__':
    check_hygiene()
