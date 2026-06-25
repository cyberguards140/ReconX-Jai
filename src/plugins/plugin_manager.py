import os
from typing import Any

import yaml


class PluginManager:
    """
    Core plugin system handling YAML-based integration definitions.
    """

    def __init__(self, plugin_dir: str = "/home/kali/ReconX/plugins"):
        self.plugin_dir = plugin_dir
        self.plugins: dict[str, Any] = {}

    def load_plugins(self):
        if not os.path.exists(self.plugin_dir):
            os.makedirs(self.plugin_dir, exist_ok=True)

        for filename in os.listdir(self.plugin_dir):
            if filename.endswith(".yaml") or filename.endswith(".yml"):
                filepath = os.path.join(self.plugin_dir, filename)
                with open(filepath) as f:
                    try:
                        plugin_def = yaml.safe_load(f)
                        plugin_id = plugin_def.get("id", filename)
                        self.plugins[plugin_id] = plugin_def
                    except Exception as e:
                        print(f"Failed to load plugin {filename}: {e}")

    def get_plugin(self, plugin_id: str) -> Any:
        return self.plugins.get(plugin_id)

    def list_plugins(self) -> list[dict[str, Any]]:
        return list(self.plugins.values())


plugin_manager = PluginManager()
