import json
import os
from datetime import datetime

SESSION_FILE = "workspace/current_project.json"


class SessionManager:
    def __init__(self):
        self.current_project = None
        self.project_id = None
        self.last_opened_project = None
        self.startup_time = datetime.now().isoformat()
        try:
            self.active_user = os.getlogin()
        except OSError:
            self.active_user = "kali"
        self._load()

    def _load(self):
        if os.path.exists(SESSION_FILE):
            try:
                with open(SESSION_FILE) as f:
                    data = json.load(f)
                    self.current_project = data.get("project")
                    self.project_id = data.get("id")
                    self.last_opened_project = data.get("last_opened_project", self.current_project)
            except Exception:
                pass

    def _save(self):
        if not os.path.exists("workspace"):
            os.makedirs("workspace")
        data = {
            "project": self.current_project,
            "id": self.project_id,
            "last_opened_project": self.last_opened_project,
            "startup_time": self.startup_time,
            "active_user": self.active_user,
        }
        with open(SESSION_FILE, "w") as f:
            json.dump(data, f)

        # Sync to dashboard state as well for easy access from legacy components
        dash_state = "dashboard_state.json"
        if os.path.exists(dash_state):
            try:
                with open(dash_state) as f:
                    d_state = json.load(f)
                d_state["project"] = self.current_project
                with open(dash_state, "w") as f:
                    json.dump(d_state, f)
            except Exception:
                pass

    def set_project(self, project_name, project_id=None):
        self.current_project = project_name
        self.project_id = project_id
        if project_name:
            self.last_opened_project = project_name
        self._save()

    def clear(self):
        self.current_project = None
        self.project_id = None
        self._save()
