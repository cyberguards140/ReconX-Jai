import pytest
from reconx.plugins.adapters.whatweb_adapter import WhatwebAdapter
from reconx.plugins.adapters.wafw00f_adapter import Wafw00fAdapter
from reconx.modules.web_fingerprinting.orchestrator import WebFingerprintingOrchestrator
from reconx.modules.web_fingerprinting.profiles import WebProfile

@pytest.mark.asyncio
async def test_whatweb_adapter_standard():
    adapter = WhatwebAdapter()
    cmd = await adapter.build_command("http://example.com")
    assert "whatweb" in cmd
    assert "-a" not in cmd

@pytest.mark.asyncio
async def test_whatweb_adapter_aggressive():
    adapter = WhatwebAdapter()
    cmd = await adapter.build_command("http://example.com", mode="aggressive")
    assert "whatweb" in cmd
    assert "-a" in cmd
    assert "3" in cmd

@pytest.mark.asyncio
async def test_wafw00f_adapter_command():
    adapter = Wafw00fAdapter()
    cmd = await adapter.build_command("http://example.com")
    assert "wafw00f" in cmd
    assert "http://example.com" in cmd

@pytest.mark.asyncio
async def test_web_orchestrator_deep():
    result = await WebFingerprintingOrchestrator.run_web_recon("http://example.com", WebProfile.DEEP)
    assert result["status"] == "scheduled"
    assert "whatweb" in result["tasks"]
    assert "wafw00f" in result["tasks"]
