import pytest
import asyncio
from reconx.plugins.registry import PluginRegistry
from reconx.plugins.manager import PluginManager
from reconx.plugins.base import ExecutionContext

@pytest.mark.asyncio
async def test_dummy_adapter_lifecycle():
    registry = PluginRegistry()
    registry.discover_and_load()
    
    # 1. Registration
    assert "dummy" in registry.list_plugins()
    
    # 2. Capabilities
    capabilities = registry.get_capabilities("dummy")
    assert capabilities["name"] == "dummy"
    assert capabilities["category"] == "test"
    
    manager = PluginManager(registry)
    
    # 3. Execution (This validates discovery, version, command gen, execution, parsing, normalization, saving)
    result = await manager.execute("dummy", "example.com")
    
    # 4. Assertions
    assert result.success is True
    assert result.plugin == "dummy"
    assert result.execution_time > 0
    assert "Dummy scan against example.com" in result.output["raw"]
    
    assert len(result.assets) == 1
    assert result.assets[0]["type"] == "dummy"
    assert result.assets[0]["value"] == "Dummy scan against example.com"

@pytest.mark.asyncio
async def test_health_check_framework():
    from reconx.plugins.health import HealthCheckFramework
    registry = PluginRegistry()
    registry.discover_and_load()
    
    health = HealthCheckFramework(registry)
    results = await health.check_all()
    
    dummy_res = next((r for r in results if r["tool"] == "dummy"), None)
    assert dummy_res is not None
    assert dummy_res["installed"] is True
