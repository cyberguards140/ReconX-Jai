import json
import os

PROJECTS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "projects")


class WorkspaceLoader:
    def create_workspace(self, project_name):
        base_path = os.path.join(PROJECTS_DIR, project_name)
        dirs = [
            "config",
            "assets",
            "findings",
            "screenshots",
            "reports",
            "logs",
            "jobs",
            "history",
            "exports",
        ]
        for d in dirs:
            os.makedirs(os.path.join(base_path, d), exist_ok=True)

        with open(os.path.join(base_path, "project.json"), "w") as f:
            json.dump({"name": project_name}, f)

        return base_path
