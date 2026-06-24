import pytest
from reconx.plugins.adapters.dnsrecon_adapter import DnsreconAdapter
from reconx.plugins.adapters.whois_adapter import WhoisAdapter
from reconx.modules.dns.orchestrator import DNSOrchestrator
from reconx.modules.dns.profiles import DNSProfile

@pytest.mark.asyncio
async def test_dnsrecon_adapter_command():
    adapter = DnsreconAdapter()
    cmd = await adapter.build_command("example.com")
    assert "dnsrecon" in cmd
    assert "example.com" in cmd

@pytest.mark.asyncio
async def test_whois_adapter_command():
    adapter = WhoisAdapter()
    cmd = await adapter.build_command("example.com")
    assert "whois" in cmd
    assert "example.com" in cmd

@pytest.mark.asyncio
async def test_dns_orchestrator():
    result = await DNSOrchestrator.run_dns_recon("example.com", DNSProfile.DEEP)
    assert result["status"] == "scheduled"
    assert "fierce" in result["tasks"]
    assert "dig" in result["tasks"]
    assert "whois" in result["tasks"]
