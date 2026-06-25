import pytest
from reconx.plugins.adapters.nuclei_adapter import NucleiAdapter
from reconx.plugins.adapters.searchsploit_adapter import SearchsploitAdapter
from reconx.modules.vulnerability_intelligence.orchestrator import VulnOrchestrator
from reconx.modules.vulnerability_intelligence.enrichment import VulnEnricher
from reconx.modules.vulnerability_intelligence.cve_mapper import CVEMapper
from reconx.modules.vulnerability_intelligence.risk_engine import RiskEngine
from reconx.modules.vulnerability_intelligence.correlator import VulnCorrelator

@pytest.mark.asyncio
async def test_nuclei_adapter_command():
    adapter = NucleiAdapter()
    cmd = await adapter.build_command("https://example.com")
    assert "nuclei" in cmd
    assert "-u" in cmd
    assert "https://example.com" in cmd
    assert "-json-export" in cmd

@pytest.mark.asyncio
async def test_searchsploit_adapter_command():
    adapter = SearchsploitAdapter()
    cmd = await adapter.build_command("Apache 2.4.49")
    assert "searchsploit" in cmd
    assert "Apache 2.4.49" in cmd
    assert "--json" in cmd

@pytest.mark.asyncio
async def test_vuln_orchestrator_asset():
    result = await VulnOrchestrator.run_vuln_analysis("https://example.com")
    assert result["status"] == "scheduled"
    assert result["target_type"] == "asset"
    assert "nuclei" in result["tasks"]

@pytest.mark.asyncio
async def test_vuln_orchestrator_technology():
    result = await VulnOrchestrator.run_vuln_analysis("Apache 2.4.49")
    assert result["status"] == "scheduled"
    assert result["target_type"] == "technology"
    assert "searchsploit" in result["tasks"]

def test_vuln_enricher_heuristics():
    assert VulnEnricher.is_technology("Apache 2.4.49") is True
    assert VulnEnricher.is_technology("nginx 1.18.0") is True
    assert VulnEnricher.is_technology("https://example.com") is False
    assert VulnEnricher.is_technology("10.10.10.10") is False

def test_cve_mapper():
    cpe = CVEMapper.map_technology("Apache", "2.4.49")
    assert cpe == "cpe:2.3:a:apache:apache:2.4.49:*:*:*:*:*:*:*"

def test_risk_engine():
    # 1 critical (10), 1 high (7), 1 medium (4) = 21 / 3 = 7.0
    score = RiskEngine.calculate_asset_risk(1, 1, 1)
    assert score == 7.0

def test_vuln_correlator_merge():
    findings = [
        {"asset_id": "asset1", "title": "TLS Weakness", "sources": ["sslscan"]},
        {"asset_id": "asset1", "title": "TLS Weakness", "sources": ["nuclei"]}
    ]
    merged = VulnCorrelator.merge_findings(findings)
    assert len(merged) == 1
    assert "sslscan" in merged[0]["sources"]
    assert "nuclei" in merged[0]["sources"]
