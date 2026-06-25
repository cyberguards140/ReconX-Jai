import pytest
from reconx.plugins.adapters.nmap_adapter import NmapAdapter
from reconx.plugins.adapters.masscan_adapter import MasscanAdapter
from reconx.plugins.adapters.netdiscover_adapter import NetdiscoverAdapter
from reconx.plugins.adapters.arpscan_adapter import ArpscanAdapter
from reconx.plugins.adapters.fping_adapter import FpingAdapter
from reconx.plugins.adapters.traceroute_adapter import TracerouteAdapter
from reconx.modules.network.orchestrator import NetworkOrchestrator
from reconx.modules.network.profiles import ScanProfile

@pytest.mark.asyncio
async def test_nmap_adapter_command():
    adapter = NmapAdapter()
    cmd = await adapter.build_command("192.168.1.1", mode="deep")
    assert "-oX" in cmd
    assert "-sV" in cmd
    assert "-O" in cmd

@pytest.mark.asyncio
async def test_masscan_adapter_command():
    adapter = MasscanAdapter()
    cmd = await adapter.build_command("10.0.0.0/24", ports="80,443")
    assert "masscan" in cmd
    assert "-oJ" in cmd

@pytest.mark.asyncio
async def test_fping_adapter_command():
    adapter = FpingAdapter()
    cmd = await adapter.build_command("127.0.0.1")
    assert "fping" in cmd
    assert "-a" in cmd

@pytest.mark.asyncio
async def test_arpscan_adapter_command():
    adapter = ArpscanAdapter()
    cmd = await adapter.build_command("192.168.1.0/24")
    assert "arp-scan" in cmd

@pytest.mark.asyncio
async def test_network_orchestrator():
    # Test orchestrator building standard profile workflow
    result = await NetworkOrchestrator.run_network_recon("192.168.1.1", ScanProfile.STANDARD)
    assert result["status"] == "scheduled"
    assert "fping" in result["tasks"]
    assert "masscan" in result["tasks"]
    assert "nmap" in result["tasks"]
