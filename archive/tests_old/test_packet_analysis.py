import pytest
from reconx.plugins.adapters.tshark_adapter import TsharkAdapter
from reconx.plugins.adapters.tcpdump_adapter import TcpdumpAdapter
from reconx.plugins.adapters.ngrep_adapter import NgrepAdapter
from reconx.modules.packet_analysis.orchestrator import PacketOrchestrator
from reconx.modules.packet_analysis.capture import CaptureSource
from reconx.modules.packet_analysis.correlation import PacketCorrelation

@pytest.mark.asyncio
async def test_tshark_adapter_command():
    adapter = TsharkAdapter()
    cmd = await adapter.build_command("capture.pcap")
    assert "tshark" in cmd
    assert "-r" in cmd
    assert "capture.pcap" in cmd
    assert "json" in cmd

@pytest.mark.asyncio
async def test_tcpdump_adapter_command():
    adapter = TcpdumpAdapter()
    cmd = await adapter.build_command("eth0")
    assert "tcpdump" in cmd
    assert "eth0" in cmd

@pytest.mark.asyncio
async def test_ngrep_adapter_command():
    adapter = NgrepAdapter()
    cmd = await adapter.build_command("capture.pcap")
    assert "ngrep" in cmd
    assert "capture.pcap" in cmd

@pytest.mark.asyncio
async def test_packet_orchestrator_offline():
    result = await PacketOrchestrator.run_packet_analysis("capture.pcap")
    assert result["status"] == "scheduled"
    assert result["mode"] == "offline"
    assert "tshark" in result["tasks"]
    assert "ngrep" in result["tasks"]

@pytest.mark.asyncio
async def test_packet_orchestrator_live():
    result = await PacketOrchestrator.run_packet_analysis("eth0")
    assert result["status"] == "scheduled"
    assert result["mode"] == "live"
    assert "tcpdump" in result["tasks"]
    assert "ngrep" in result["tasks"]

def test_capture_source_heuristics():
    assert CaptureSource.is_pcap("traffic.pcap") is True
    assert CaptureSource.is_pcap("traffic.pcapng") is True
    assert CaptureSource.is_interface("eth0") is True
    assert CaptureSource.is_interface("wlan0") is True
    # If not a pcap, default to interface
    assert CaptureSource.is_interface("enp3s0") is True

def test_packet_correlation():
    mapped = PacketCorrelation.map_flow_to_asset("10.10.10.5", "10.10.10.10")
    assert mapped["source"] == "10.10.10.5"
    assert mapped["target"] == "10.10.10.10"
    assert mapped["type"] == "communicates_with"
