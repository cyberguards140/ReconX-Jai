import yaml
import os

CONFIG_FILE = "config/config.yaml"
DEFAULT_CONFIG = {
    "theme": "dark",
    "dashboard_port": 3000,
    "auto_open_browser": True,
    "log_level": "info"
}

class ConfigLoader:
    def __init__(self):
        self.config = DEFAULT_CONFIG.copy()
        self.load()

    def load(self):
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, 'r') as f:
                    data = yaml.safe_load(f)
                    if data:
                        self.config.update(data)
            except Exception:
                pass

    def get(self, key, default=None):
        return self.config.get(key, default)
