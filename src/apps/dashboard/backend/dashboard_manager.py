import json
import os
import threading
import webbrowser
from datetime import datetime

STATE_FILE = "dashboard_state.json"


class DashboardManager:
    def __init__(self, port=3000, auto_open=True):
        self.port = port
        self.auto_open = auto_open
        self.server_thread = None

    def _save_state(self, project_name):
        state = {
            "running": True,
            "port": self.port,
            "project": project_name,
            "started": datetime.now().isoformat(),
        }
        with open(STATE_FILE, "w") as f:
            json.dump(state, f)

    def _update_project(self, project_name):
        if os.path.exists(STATE_FILE):
            try:
                with open(STATE_FILE) as f:
                    state = json.load(f)
                state["project"] = project_name
                with open(STATE_FILE, "w") as f:
                    json.dump(state, f)
            except Exception:
                self._save_state(project_name)
        else:
            self._save_state(project_name)

    def start(self, project_name="None"):
        self._update_project(project_name)

        if self.server_thread and self.server_thread.is_alive():
            print("\n[!] Dashboard already running.")
            print("[+] Opening existing instance...")
            if self.auto_open:
                try:
                    webbrowser.open(f"http://127.0.0.1:8000/dashboard")
                except Exception:
                    pass
            return

        print("\n[+] Loading ReconX Dashboard...")
        print("[+] Connecting Backend...")
        print("[+] Loading Project...")
        print("[+] Starting UI...")

        import subprocess
        import sys

        def run():
            try:
                subprocess.Popen(
                    [sys.executable, "-m", "apps.cli.main", "api"],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                )
            except Exception as e:
                print(
                    f"\n[-] Failed to start dashboard. Possible causes:\n• Port already in use\n• Flask missing\n• Browser launch failure\nError: {e}"
                )

        self.server_thread = threading.Thread(target=run, daemon=True)
        self.server_thread.start()

        if self.auto_open:
            try:
                webbrowser.open(f"http://127.0.0.1:8000/dashboard")
            except Exception:
                pass
