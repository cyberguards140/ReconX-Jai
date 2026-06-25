import pytest
from reconx.plugins.adapters.netexec_adapter import NetexecAdapter
from reconx.plugins.adapters.ldapsearch_adapter import LdapsearchAdapter
from reconx.plugins.adapters.kerbrute_adapter import KerbruteAdapter
from reconx.plugins.adapters.bloodhound_adapter import BloodhoundAdapter
from reconx.modules.active_directory.orchestrator import ADOrchestrator
from reconx.modules.active_directory.profiles import ADProfile
from reconx.modules.active_directory.enrichment import ADEnricher
from reconx.modules.active_directory.graph import ADGraphBuilder

@pytest.mark.asyncio
async def test_netexec_adapter_command():
    adapter = NetexecAdapter()
    cmd = await adapter.build_command("10.10.10.6")
    assert "netexec" in cmd
    assert "smb" in cmd
    assert "10.10.10.6" in cmd

@pytest.mark.asyncio
async def test_ldapsearch_adapter_command():
    adapter = LdapsearchAdapter()
    cmd = await adapter.build_command("10.10.10.6")
    assert "ldapsearch" in cmd
    assert "ldap://10.10.10.6" in cmd

@pytest.mark.asyncio
async def test_kerbrute_adapter_command():
    adapter = KerbruteAdapter()
    cmd = await adapter.build_command("10.10.10.6")
    assert "kerbrute" in cmd
    assert "userenum" in cmd
    assert "10.10.10.6" in cmd

@pytest.mark.asyncio
async def test_bloodhound_adapter_command():
    adapter = BloodhoundAdapter()
    cmd = await adapter.build_command("10.10.10.6")
    assert "bloodhound-python" in cmd
    assert "-c" in cmd
    assert "All" in cmd

@pytest.mark.asyncio
async def test_ad_orchestrator_deep():
    result = await ADOrchestrator.run_ad_recon("10.10.10.6", ADProfile.DEEP)
    assert result["status"] == "scheduled"
    assert "netexec" in result["tasks"]
    assert "ldapsearch" in result["tasks"]
    assert "kerbrute" in result["tasks"]
    assert "bloodhound" in result["tasks"]

def test_ad_enricher():
    assert ADEnricher.is_ad_service(389) is True
    assert ADEnricher.is_ad_service(88) is True
    assert ADEnricher.is_ad_service(443) is False

def test_ad_graph_builder():
    mapped = ADGraphBuilder.map_to_asset("DC01", "10.10.10.6")
    assert mapped["hostname"] == "DC01"
    assert mapped["ip"] == "10.10.10.6"
    assert mapped["relationship"] == "resolves_to"
