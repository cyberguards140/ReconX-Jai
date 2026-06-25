import importlib.util
import json
import os


class PluginLoader:
    @staticmethod
    def discover_plugins(plugin_dir="plugins/installed"):
        discovered = []
        if not os.path.exists(plugin_dir):
            return discovered

        for d in os.listdir(plugin_dir):
            path = os.path.join(plugin_dir, d)
            if os.path.isdir(path):
                manifest_path = os.path.join(path, "manifest.json")
                if os.path.exists(manifest_path):
                    with open(manifest_path) as f:
                        try:
                            manifest = json.load(f)
                            manifest["_path"] = path
                            discovered.append(manifest)
                        except Exception:
                            pass
        return discovered

    @staticmethod
    def load_plugin(manifest):
        path = manifest.get("_path")
        plugin_file = os.path.join(path, "plugin.py")

        if not os.path.exists(plugin_file):
            return None

        spec = importlib.util.spec_from_file_location(manifest["name"], plugin_file)
        module = importlib.util.module_from_spec(spec)
        try:
            spec.loader.exec_module(module)
            return module
        except Exception as e:
            print(f"Error loading plugin {manifest['name']}: {e}")
            return None
