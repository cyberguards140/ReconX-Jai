import pytest
from reconx.plugins.adapters.gobuster_adapter import GobusterAdapter
from reconx.plugins.adapters.ffuf_adapter import FfufAdapter
from reconx.modules.content_discovery.orchestrator import ContentDiscoveryOrchestrator
from reconx.modules.content_discovery.profiles import ContentProfile

@pytest.mark.asyncio
async def test_gobuster_adapter_command():
    adapter = GobusterAdapter()
    cmd = await adapter.build_command("http://example.com")
    assert "gobuster" in cmd
    assert "dir" in cmd
    assert "http://example.com" in cmd

@pytest.mark.asyncio
async def test_ffuf_adapter_command():
    adapter = FfufAdapter()
    cmd = await adapter.build_command("http://example.com")
    assert "ffuf" in cmd
    assert "http://example.com/FUZZ" in cmd

@pytest.mark.asyncio
async def test_content_orchestrator_deep():
    result = await ContentDiscoveryOrchestrator.run_content_recon("http://example.com", ContentProfile.DEEP)
    assert result["status"] == "scheduled"
    assert "gobuster" in result["tasks"]
    assert "ffuf" in result["tasks"]
    assert "wfuzz" in result["tasks"]
