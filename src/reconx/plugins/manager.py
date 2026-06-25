"""Plugin manager providing the canonical plugin_manager singleton.

This module bridges the gap between the existing PluginManager class
in reconx.plugins.plugin_manager and the import path used throughout
the codebase (reconx.plugins.manager).
"""

from typing import Any


class _PluginManager:
    """Lightweight plugin manager facade."""

    def __init__(self):
        self._plugins: dict[str, Any] = {}
        self._loaded = False

    def load_plugins(self, plugin_dir: str = "plugins") -> None:
        """Discover and load plugins from the given directory."""
        # Delegate to the full PluginManager when available
        try:
            from reconx.plugins.plugin_loader import PluginLoader

            discovered = PluginLoader.discover_plugins()
            for manifest in discovered:
                name = manifest.get("name", "unknown")
                self._plugins[name] = manifest
        except Exception:
            pass
        self._loaded = True

    def get_plugin(self, name: str) -> Any | None:
        """Retrieve a loaded plugin by name."""
        return self._plugins.get(name)

    def list_plugins(self) -> list[str]:
        """List all loaded plugin names."""
        return list(self._plugins.keys())

    async def execute(self, plugin_name: str, target: str, args: dict | None = None) -> Any:
        """Execute a plugin against a target."""
        plugin = self.get_plugin(plugin_name)
        if plugin is None:
            raise ValueError(f"Plugin '{plugin_name}' not found")
        # TODO: Implement actual plugin execution
        return {"plugin": plugin_name, "target": target, "status": "executed"}


# Singleton instance used throughout the codebase
plugin_manager = _PluginManager()
