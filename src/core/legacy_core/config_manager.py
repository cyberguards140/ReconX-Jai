import os
import json
from core.legacy_core.session import SessionManager

class ConfigManager:
    @staticmethod
    def get_config_path(project_id, tool_id):
        proj_dir = os.path.join("projects", project_id, "logs")
        if not os.path.exists(proj_dir):
            os.makedirs(proj_dir, exist_ok=True)
        return os.path.join(proj_dir, f"{tool_id}_config.json")

    @staticmethod
    def load_config(tool_id):
        session = SessionManager()
        if not session.current_project:
            return {}
            
        path = ConfigManager.get_config_path(session.current_project, tool_id)
        if os.path.exists(path):
            try:
                with open(path, 'r') as f:
                    return json.load(f)
            except:
                pass
        return {}

    @staticmethod
    def save_config(tool_id, config_dict):
        session = SessionManager()
        if not session.current_project:
            return False
            
        path = ConfigManager.get_config_path(session.current_project, tool_id)
        try:
            with open(path, 'w') as f:
                json.dump(config_dict, f, indent=2)
            return True
        except:
            return False
