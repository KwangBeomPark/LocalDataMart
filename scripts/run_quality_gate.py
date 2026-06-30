import subprocess
import sys
import argparse
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent


def run_step(command_list, step_name):
    print(f"\n---> Running Step: {step_name} ...", flush=True)
    try:
        subprocess.run(
            command_list,
            check=True,
            cwd=PROJECT_ROOT,
            stderr=subprocess.STDOUT,
        )
        print(f"[PASS] {step_name} completed successfully.", flush=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"[FAIL] {step_name} failed with exit code {e.returncode}.", flush=True)
        return False

def main():
    parser = argparse.ArgumentParser(description="Local Quality Gate for Finance DataMart Tool")
    parser.add_argument("--skip-hygiene", action="store_true", help="Skip release hygiene check step")
    args = parser.parse_args()

    print("=============================================", flush=True)
    print("=== Finance DataMart Quality Gate Console ===", flush=True)
    print("=============================================", flush=True)

    steps = []

    # Step 1: Release Hygiene Check
    if not args.skip_hygiene:
        steps.append(([sys.executable, 'scripts/check_release_hygiene.py'], "Release Hygiene Check"))
    else:
        print("[INFO] Skipping Release Hygiene Check as requested.", flush=True)

    # Step 2: Python Code Compilation Check
    steps.append(([sys.executable, '-m', 'compileall', 'app', 'scripts'], "Python Code Compilation Check"))

    # Step 3: Generate Sample Data
    steps.append(([sys.executable, 'scripts/create_sample_data.py'], "Generate Sample Data"))

    # Step 4: Run Main DataMart Pipeline
    steps.append(([sys.executable, '-m', 'app.main'], "Run Main DataMart Pipeline"))

    # Step 5: Generate Column Inventory
    steps.append(([sys.executable, 'scripts/create_column_inventory.py'], "Generate Column Inventory"))

    # Step 6: Run Pre-release Integrity Check
    steps.append(([sys.executable, 'scripts/pre_release_check.py'], "Run Pre-release Integrity Check"))

    # Step 7: Verify UI Package Import
    steps.append(([sys.executable, '-c', "from app.ui_app import DataMartUI; print('UI import ok')"], "Verify UI Package Import"))

    for cmd, name in steps:
        success = run_step(cmd, name)
        if not success:
            print("\n=============================================", flush=True)
            print("[GATE FAIL] Quality gate blocked at: " + name, flush=True)
            print("=============================================", flush=True)
            sys.exit(1)

    print("\n=============================================", flush=True)
    print("Quality gate PASS", flush=True)
    print("=============================================", flush=True)
    sys.exit(0)

if __name__ == '__main__':
    main()
