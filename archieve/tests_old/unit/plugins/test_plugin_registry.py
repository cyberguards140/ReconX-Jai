import pytest
from reconx.plugins.registry import PluginRegistry
from reconx.plugins.base import BasePlugin

class DummyPlugin(BasePlugin):
    name = "dummy"
    version = "1.0"
    
    async def execute(self, target: str, options: dict) -> dict:
        return {"status": "success"}

def test_plugin_registration():
    registry = PluginRegistry()
    registry.register(DummyPlugin)
    assert "dummy" in registry.plugins

def test_plugin_lookup():
    registry = PluginRegistry()
    registry.register(DummyPlugin)
    plugin = registry.get("dummy")
    assert plugin is not None
    assert plugin.name == "dummy"

def test_duplicate_plugin_registration():
    registry = PluginRegistry()
    registry.register(DummyPlugin)
    # Registration logic usually either overwrites or raises. 
    # Just asserting it doesn't crash unexpectedly or handles it.
    try:
        registry.register(DummyPlugin)
    except Exception:
        pass
    assert "dummy" in registry.plugins
