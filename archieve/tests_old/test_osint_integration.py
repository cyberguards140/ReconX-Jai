import pytest
from reconx.plugins.adapters.reconng_adapter import ReconngAdapter
from reconx.plugins.adapters.sherlock_adapter import SherlockAdapter
from reconx.plugins.adapters.holehe_adapter import HoleheAdapter
from reconx.modules.osint.orchestrator import OSINTOrchestrator
from reconx.modules.osint.profiles import OSINTProfile
from reconx.modules.osint.enrichment import OSINTEnricher
from reconx.modules.osint.correlation import OSINTCorrelation

@pytest.mark.asyncio
async def test_reconng_adapter_command():
    adapter = ReconngAdapter()
    cmd = await adapter.build_command("example.com")
    assert "recon-cli" in cmd
    assert "-C" in cmd
    assert "modules load" in cmd[2]

@pytest.mark.asyncio
async def test_sherlock_adapter_command():
    adapter = SherlockAdapter()
    cmd = await adapter.build_command("admin_user")
    assert "sherlock" in cmd
    assert "admin_user" in cmd

@pytest.mark.asyncio
async def test_holehe_adapter_command():
    adapter = HoleheAdapter()
    cmd = await adapter.build_command("admin@example.com")
    assert "holehe" in cmd
    assert "admin@example.com" in cmd

@pytest.mark.asyncio
async def test_osint_orchestrator_deep():
    result = await OSINTOrchestrator.run_osint_recon("example.com", OSINTProfile.DEEP)
    assert result["status"] == "scheduled"
    assert "theharvester" in result["tasks"]
    assert "reconng" in result["tasks"]
    assert "holehe" in result["tasks"]
    assert "sherlock" in result["tasks"]

def test_osint_enricher():
    assert OSINTEnricher.is_email("admin@example.com") is True
    assert OSINTEnricher.is_email("admin_user") is False
    assert OSINTEnricher.is_username("admin_user") is True
    assert OSINTEnricher.is_username("admin@example.com") is False

def test_osint_correlation():
    mapped = OSINTCorrelation.link_org_to_domain("Example Corp", "example.com")
    assert mapped["source"] == "Example Corp"
    assert mapped["target"] == "example.com"
    assert mapped["type"] == "owns"
