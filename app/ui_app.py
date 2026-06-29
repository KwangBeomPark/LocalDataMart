import os
import re
import sys
import tkinter as tk
from tkinter import messagebox
from pathlib import Path
import subprocess
import threading

PROJECT_ROOT = Path(__file__).resolve().parent.parent


class DataMartUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Finance DataMart Tool - Desktop Home")
        self.root.geometry("520x390")
        self.root.resizable(False, False)
        
        # 기본 경로 설정
        self.workspace_dir = PROJECT_ROOT / "sample_workspace"
        self.output_dir = self.workspace_dir / "04_Report_View"
        self.log_dir = self.workspace_dir / "99_Logs"
        self.config_file = self.workspace_dir / "90_Config" / "config.xlsx"
        self.validation_log = self.log_dir / "validation_log.csv"
        
        # 처리 중인 상태 플래그
        self.is_processing = False
        
        self._build_ui()
        self._update_log_status()

    def _sanitize_message(self, value) -> str:
        text = "" if value is None else str(value)
        replacements = [
            str(PROJECT_ROOT),
            str(PROJECT_ROOT).replace("\\", "/"),
            str(Path.home()),
            str(Path.home()).replace("\\", "/"),
        ]
        for path_text in replacements:
            if path_text:
                text = text.replace(path_text, "[local_path]")
        return re.sub(r"[A-Za-z]:[\\/][^\s,\")']+", "[local_path]", text)

    def _build_ui(self):
        # 상단 타이틀 프레임
        title_frame = tk.Frame(self.root, bg="#2c3e50", height=60)
        title_frame.pack(fill=tk.X)
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(
            title_frame, 
            text="Finance DataMart Control Panel", 
            font=("Helvetica", 14, "bold"), 
            fg="#ecf0f1", 
            bg="#2c3e50"
        )
        title_label.pack(pady=15)
        
        # 메인 버튼 컨테이너 프레임
        button_frame = tk.Frame(self.root, padx=20, pady=20)
        button_frame.pack(fill=tk.BOTH, expand=True)
        
        # 왼쪽: 데이터 정제 및 분석 처리 버튼들
        proc_lf = tk.LabelFrame(button_frame, text="Data Mart Processing", font=("Helvetica", 9, "bold"), padx=10, pady=10)
        proc_lf.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        self.btn_refresh = tk.Button(
            proc_lf, 
            text="Refresh DataMart", 
            command=self.on_refresh, 
            font=("Helvetica", 10, "bold"),
            bg="#27ae60",
            fg="white",
            height=2
        )
        self.btn_refresh.pack(fill=tk.X, pady=8)
        
        self.btn_inventory = tk.Button(
            proc_lf, 
            text="Generate Inventory", 
            command=self.on_generate_inventory, 
            font=("Helvetica", 10, "bold"),
            bg="#2980b9",
            fg="white",
            height=2
        )
        self.btn_inventory.pack(fill=tk.X, pady=8)
        
        self.btn_precheck = tk.Button(
            proc_lf, 
            text="Run Pre-release Check", 
            command=self.on_pre_release_check, 
            font=("Helvetica", 10, "bold"),
            bg="#e67e22",
            fg="white",
            height=2
        )
        self.btn_precheck.pack(fill=tk.X, pady=8)
        
        # 오른쪽: 탐색 및 파일 열기 버튼들
        open_lf = tk.LabelFrame(button_frame, text="Quick Shortcuts", font=("Helvetica", 9, "bold"), padx=10, pady=10)
        open_lf.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(10, 0))
        
        self.btn_open_config = tk.Button(
            open_lf, 
            text="Open Config File", 
            command=self.on_open_config, 
            font=("Helvetica", 10),
            height=1
        )
        self.btn_open_config.pack(fill=tk.X, pady=5)
        
        self.btn_open_output = tk.Button(
            open_lf, 
            text="Open Output Folder", 
            command=self.on_open_output, 
            font=("Helvetica", 10),
            height=1
        )
        self.btn_open_output.pack(fill=tk.X, pady=5)
        
        self.btn_open_log = tk.Button(
            open_lf, 
            text="Open Log Folder", 
            command=self.on_open_log, 
            font=("Helvetica", 10),
            height=1
        )
        self.btn_open_log.pack(fill=tk.X, pady=5)
        
        # 하단 상태 바 (Status Bar)
        self.status_bar = tk.Frame(self.root, bd=1, relief=tk.SUNKEN, padx=5, pady=5)
        self.status_bar.pack(fill=tk.X, side=tk.BOTTOM)
        
        self.status_label = tk.Label(
            self.status_bar, 
            text="Status: Ready", 
            font=("Helvetica", 9, "bold"), 
            fg="#7f8c8d"
        )
        self.status_label.pack(anchor=tk.W)
        
        self.log_info_label = tk.Label(
            self.status_bar, 
            text="Log: -", 
            font=("Helvetica", 8), 
            fg="#95a5a6"
        )
        self.log_info_label.pack(anchor=tk.W, pady=(2, 0))

    def _set_buttons_state(self, state):
        self.btn_refresh.config(state=state)
        self.btn_inventory.config(state=state)
        self.btn_precheck.config(state=state)
        self.btn_open_config.config(state=state)
        self.btn_open_output.config(state=state)
        self.btn_open_log.config(state=state)

    def _update_log_status(self):
        """최근 검증 로그 파일 위치 및 상태를 표시합니다."""
        if self.validation_log.exists():
            mod_time = datetime_str = ""
            try:
                mtime = os.path.getmtime(self.validation_log)
                from datetime import datetime
                datetime_str = datetime.fromtimestamp(mtime).strftime("%Y-%m-%d %H:%M:%S")
            except Exception:
                pass
            self.log_info_label.config(
                text=f"Recent Log: {self.validation_log.name} (Updated: {datetime_str})"
            )
        else:
            self.log_info_label.config(text="Recent Log: None (run Refresh first)")

    def _run_module_async(self, target_func, task_name):
        if self.is_processing:
            messagebox.showinfo("Running", "Another task is already running.")
            return

        self.is_processing = True
        self._set_buttons_state(tk.DISABLED)
        self.status_label.config(text=f"Status: Running {task_name}...", fg="#d35400")
        
        def run():
            try:
                target_func()
                self.root.after(0, lambda: self._on_task_success(task_name))
            except SystemExit as se:
                if se.code == 0 or se.code is None:
                    self.root.after(0, lambda: self._on_task_success(task_name))
                else:
                    safe_err = f"SystemExit code {se.code}"
                    self.root.after(0, lambda: self._on_task_error(task_name, safe_err))
            except Exception as e:
                safe_err = self._sanitize_message(e)
                self.root.after(0, lambda: self._on_task_error(task_name, safe_err))
                
        threading.Thread(target=run, daemon=True).start()

    def run_refresh_logic(self):
        from app.main import main as run_pipeline
        run_pipeline()

    def run_inventory_logic(self):
        from app.column_inventory import ColumnInventoryGenerator
        generator = ColumnInventoryGenerator(
            config_path="sample_workspace/90_Config/config.xlsx",
            output_path="sample_workspace/90_Config/column_inventory.xlsx"
        )
        generator.generate()

    def run_prerelease_logic(self):
        from scripts.pre_release_check import PreReleaseChecker
        checker = PreReleaseChecker()
        success = checker.run_checks()
        if not success:
            raise RuntimeError("Pre-release check detected failures.")

    def _on_task_success(self, task_name):
        self.is_processing = False
        self._set_buttons_state(tk.NORMAL)
        self.status_label.config(text=f"Status: {task_name} Finished Successfully", fg="#27ae60")
        self._update_log_status()
        messagebox.showinfo("Success", f"{task_name} completed successfully!")

    def _on_task_error(self, task_name, error_msg):
        self.is_processing = False
        self._set_buttons_state(tk.NORMAL)
        self.status_label.config(text=f"Status: {task_name} Failed", fg="#c0392b")
        self._update_log_status()
        messagebox.showerror("Error", f"Failed to execute {task_name}.\n\nReason: {error_msg}")

    # --- 버튼 핸들러 ---
    def on_refresh(self):
        self._run_module_async(self.run_refresh_logic, "Refresh DataMart")

    def on_generate_inventory(self):
        self._run_module_async(self.run_inventory_logic, "Generate Column Inventory")

    def on_pre_release_check(self):
        self._run_module_async(self.run_prerelease_logic, "Pre-release Check")

    def _open_path(self, path, is_file=False):
        """지정된 경로를 Windows 탐색기 혹은 기본 연결 프로그램으로 안전하게 엽니다."""
        abs_path = Path(path).resolve()
        if not abs_path.exists():
            messagebox.showwarning("Warning", f"Path does not exist: {self._sanitize_message(abs_path)}")
            return
            
        try:
            # 윈도우 표준 파일/폴더 셸 오프너 기동
            os.startfile(abs_path)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open path: {self._sanitize_message(e)}")

    def on_open_config(self):
        self._open_path(self.config_file, is_file=True)

    def on_open_output(self):
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self._open_path(self.output_dir)

    def on_open_log(self):
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self._open_path(self.log_dir)

def launch():
    root = tk.Tk()
    app = DataMartUI(root)
    root.mainloop()

FinanceDataMartApp = DataMartUI

if __name__ == "__main__":
    launch()
