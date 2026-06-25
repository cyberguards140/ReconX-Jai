import pytest
import asyncio
from unittest.mock import AsyncMock, patch
from reconx.plugins.base import BasePlugin, PluginResult, ExecutionContext

class HttpxAdapter(BasePlugin):
    async def execute(self, target: str, context: ExecutionContext = None) -> PluginResult:
        import asyncio
        proc = await asyncio.create_subprocess_exec("httpx", target)
        await proc.communicate()
        return PluginResult(success=True, plugin="test", execution_time=0.1, output={})

@pytest.mark.asyncio
@patch('asyncio.create_subprocess_exec')
async def test_mock_external_tool(mock_exec):
    mock_process = AsyncMock()
    mock_process.communicate.return_value = (b'{"status": "open"}', b'')
    mock_process.returncode = 0
    mock_exec.return_value = mock_process

    adapter = HttpxAdapter()
    result = await adapter.execute("example.com", ExecutionContext())
    
    assert result is not None
    mock_exec.assert_called_once()
