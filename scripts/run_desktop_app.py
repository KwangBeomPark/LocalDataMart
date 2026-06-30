import sys
import re
from pathlib import Path

def sanitize_message(value) -> str:
    text = "" if value is None else str(value)
    try:
        home_dir = str(Path.home())
        replacements = [
            home_dir,
            home_dir.replace("\\", "/"),
        ]
        for path_text in replacements:
            if path_text:
                text = text.replace(path_text, "[user_home]")
    except Exception:
        pass

    text = re.sub(r"[A-Za-z]:[\\/][^\s,\")']+", "[local_path]", text)
    text = re.sub(r"File \"[^\"]+\"", 'File "[local_file]"', text)
    return text

def show_error_dialog(title, message):
    try:
        import tkinter as tk
        from tkinter import messagebox
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror(title, message)
        root.destroy()
    except Exception:
        try:
            import ctypes
            ctypes.windll.user32.MessageBoxW(0, message, title, 0x10)
        except Exception:
            print(f"[{title}] {message}", file=sys.stderr)

try:
    if getattr(sys, "frozen", False):
        root_dir = Path(sys.executable).resolve().parent
    else:
        root_dir = Path(__file__).resolve().parent.parent

    # 프로젝트 루트를 파이썬 경로에 추가
    sys.path.append(str(root_dir))

    from app.ui_app import launch
except Exception as e:
    safe_err = f"{type(e).__name__}: {sanitize_message(e)}"
    msg = (
        "The application could not start correctly. "
        "Please reinstall FinanceDataMart or run the pre-release check from the source package.\n\n"
        f"Error details: {safe_err}"
    )
    show_error_dialog("Application Initialization Error", msg)
    sys.exit(1)

def main():
    try:
        print("Launching Desktop UI App...")
        launch()
    except Exception as e:
        safe_err = f"{type(e).__name__}: {sanitize_message(e)}"
        msg = (
            "The application encountered an unexpected error and has stopped working. "
            "Please reinstall FinanceDataMart or run the pre-release check from the source package.\n\n"
            f"Error details: {safe_err}"
        )
        show_error_dialog("Application Crash", msg)
        sys.exit(1)

if __name__ == "__main__":
    main()
