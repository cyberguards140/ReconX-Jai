import pytest
import pytest_asyncio
from pathlib import Path
from reconx.plugins.manager import PluginManager
from reconx.plugins.registry import PluginRegistry
from reconx.plugins.exceptions import PluginRegistrationError, PluginValidationError
import tempfile
import yaml

@pytest.fixture
def temp_plugin_dir():
    with tempfile.TemporaryDirectory() as tmpdirname:
        yield Path(tmpdirname)


def create_mock_plugin(base_dir: Path, name: str, code: str, metadata: dict):
    plugin_dir = base_dir / name
    plugin_dir.mkdir(parents=True, exist_ok=True)
    with open(plugin_dir / "plugin.yaml", "w") as f:
        yaml.dump(metadata, f)
    with open(plugin_dir / "plugin.py", "w") as f:
        f.write(code)


@pytest.mark.asyncio
async def test_plugin_discovery(temp_plugin_dir):
    create_mock_plugin(
        temp_plugin_dir,
        "test_plugin",
        "from reconx.plugins.base import BasePlugin, PluginResult, ExecutionContext\nclass TestPlugin(BasePlugin):\n    name = 'test_plugin'\n    async def execute(self, t, context=None): return PluginResult(success=True, plugin='test_plugin', execution_time=0.1, output={})\nToolAdapter = TestPlugin\n",
        {"name": "test_plugin", "version": "1.0", "author": "test"},
    )
    registry = PluginRegistry(str(temp_plugin_dir))
    registry.discover_and_load()
    plugins = registry.list_plugins()
    assert len(plugins) == 1
    assert plugins[0] == "test_plugin"


@pytest.mark.asyncio
async def test_malformed_plugin_rejected(temp_plugin_dir):
    create_mock_plugin(
        temp_plugin_dir,
        "bad_plugin",
        "from reconx.plugins.base import BasePlugin\nclass BadPlugin(BasePlugin):\n    pass\nToolAdapter = BadPlugin\n",
        {"name": "bad_plugin", "version": "1.0", "author": "test"},
    )
    registry = PluginRegistry(str(temp_plugin_dir))
    # It should fail registration but since discover_and_load ignores errors, it won't be in list
    registry.discover_and_load()
    assert "bad_plugin" not in registry.list_plugins()
    with pytest.raises(PluginRegistrationError):
        registry.get("bad_plugin")


@pytest.mark.asyncio
async def test_plugin_execution(temp_plugin_dir):
    create_mock_plugin(
        temp_plugin_dir,
        "exec_plugin",
        """from reconx.plugins.base import BasePlugin, PluginResult, ExecutionContext
class ExecPlugin(BasePlugin):
    name = 'exec_plugin'
    async def validate(self): return True
    async def execute(self, t, context=None): return PluginResult(success=True, plugin='exec_plugin', execution_time=0.1, output={}, findings=[{"foo":"bar"}])
ToolAdapter = ExecPlugin
    """,
        {"name": "exec_plugin", "version": "1.0", "author": "test"},
    )
    manager = PluginManager(PluginRegistry(str(temp_plugin_dir)))
    result = await manager.execute("exec_plugin", "example.com")
    assert result.success is True
    assert result.findings[0]["foo"] == "bar"


@pytest.mark.asyncio
async def test_plugin_timeout(temp_plugin_dir):
    create_mock_plugin(
        temp_plugin_dir,
        "slow_plugin",
        """import asyncio
from reconx.plugins.base import BasePlugin, PluginResult, ExecutionContext
class SlowPlugin(BasePlugin):
    name = 'slow_plugin'
    async def validate(self): return True
    async def execute(self, t, context=None):
        await asyncio.sleep(10)
        return PluginResult(success=True, plugin='slow_plugin', execution_time=0.1, output={})
ToolAdapter = SlowPlugin
    """,
        {"name": "slow_plugin", "version": "1.0", "author": "test"},
    )
    # We load manually to monkeypatch sandbox easily
    from reconx.plugins.sandbox import PluginSandbox
    registry = PluginRegistry(str(temp_plugin_dir))
    registry.discover_and_load()
    plugin_class = registry.get("slow_plugin")
    plugin_instance = plugin_class()
    sandbox = PluginSandbox(timeout=1)
    
    with pytest.raises(Exception):
        await sandbox.execute(plugin_instance, "t")
