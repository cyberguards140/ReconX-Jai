from typing import List, Dict, Any, Optional
from reconx.plugins.manager import plugin_manager
from reconx.plugins.schemas.plugin import PluginMetadata, PluginResult

class PluginService:
    def list_plugins(self) -> List[PluginMetadata]:
        return plugin_manager.list_plugins()

    def get_plugin(self, name: str) -> Optional[PluginMetadata]:
        return plugin_manager.get_plugin(name)

    async def execute_plugin(self, name: str, target: str) -> PluginResult:
        return await plugin_manager.execute(name, target)

plugin_service = PluginService()
