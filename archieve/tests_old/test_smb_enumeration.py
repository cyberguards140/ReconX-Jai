import pytest
from reconx.plugins.adapters.enum4linuxng_adapter import Enum4linuxngAdapter
from reconx.plugins.adapters.smbclient_adapter import SmbclientAdapter
from reconx.plugins.adapters.rpcclient_adapter import RpcclientAdapter
from reconx.modules.smb.orchestrator import SMBOrchestrator
from reconx.modules.smb.profiles import SMBProfile
from reconx.modules.smb.enrichment import SMBEnricher

@pytest.mark.asyncio
async def test_enum4linuxng_adapter_command():
    adapter = Enum4linuxngAdapter()
    cmd = await adapter.build_command("10.10.10.5")
    assert "enum4linux-ng" in cmd
    assert "-A" in cmd
    assert "10.10.10.5" in cmd

@pytest.mark.asyncio
async def test_smbclient_adapter_command():
    adapter = SmbclientAdapter()
    cmd = await adapter.build_command("10.10.10.5")
    assert "smbclient" in cmd
    assert "-L" in cmd

@pytest.mark.asyncio
async def test_rpcclient_adapter_command():
    adapter = RpcclientAdapter()
    cmd = await adapter.build_command("10.10.10.5")
    assert "rpcclient" in cmd
    assert "-U" in cmd

@pytest.mark.asyncio
async def test_smb_orchestrator_deep():
    result = await SMBOrchestrator.run_smb_recon("10.10.10.5", SMBProfile.DEEP)
    assert result["status"] == "scheduled"
    assert "enum4linuxng" in result["tasks"]
    assert "smbclient" in result["tasks"]
    assert "rpcclient" in result["tasks"]

def test_smb_enricher():
    assert SMBEnricher.is_smb_service(445) is True
    assert SMBEnricher.is_smb_service(139) is True
    assert SMBEnricher.is_smb_service(80) is False
