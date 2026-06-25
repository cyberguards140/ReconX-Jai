import pytest
from reconx.plugins.adapters.amass_adapter import AmassAdapter
from reconx.plugins.adapters.theharvester_adapter import TheharvesterAdapter
from reconx.modules.subdomains.orchestrator import SubdomainOrchestrator
from reconx.modules.subdomains.profiles import SubdomainProfile

@pytest.mark.asyncio
async def test_amass_adapter_passive():
    adapter = AmassAdapter()
    cmd = await adapter.build_command("example.com", mode="passive")
    assert "amass" in cmd
    assert "-passive" in cmd

@pytest.mark.asyncio
async def test_amass_adapter_active():
    adapter = AmassAdapter()
    cmd = await adapter.build_command("example.com", mode="active")
    assert "amass" in cmd
    assert "-active" in cmd

@pytest.mark.asyncio
async def test_theharvester_adapter_command():
    adapter = TheharvesterAdapter()
    cmd = await adapter.build_command("example.com")
    assert "theHarvester" in cmd
    assert "example.com" in cmd
    assert "all" in cmd

@pytest.mark.asyncio
async def test_subdomain_orchestrator_deep():
    result = await SubdomainOrchestrator.run_subdomain_recon("example.com", SubdomainProfile.DEEP)
    assert result["status"] == "scheduled"
    assert "amass" in result["tasks"]
    assert "theharvester" in result["tasks"]
    assert "fierce" in result["tasks"]
