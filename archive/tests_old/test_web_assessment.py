import pytest
from reconx.plugins.adapters.nikto_adapter import NiktoAdapter
from reconx.plugins.adapters.testssl_adapter import TestsslAdapter
from reconx.modules.web_assessment.orchestrator import WebAssessmentOrchestrator
from reconx.modules.web_assessment.profiles import AssessmentProfile
from reconx.modules.web_assessment.findings import SeverityMapper
from reconx.database.models import SeverityEnum

@pytest.mark.asyncio
async def test_nikto_adapter_command():
    adapter = NiktoAdapter()
    cmd = await adapter.build_command("http://example.com")
    assert "nikto" in cmd
    assert "http://example.com" in cmd

@pytest.mark.asyncio
async def test_testssl_adapter_command():
    adapter = TestsslAdapter()
    cmd = await adapter.build_command("http://example.com")
    assert "testssl.sh" in cmd
    assert "--quiet" in cmd

@pytest.mark.asyncio
async def test_assessment_orchestrator_deep():
    result = await WebAssessmentOrchestrator.run_assessment("http://example.com", AssessmentProfile.DEEP)
    assert result["status"] == "scheduled"
    assert "nikto" in result["tasks"]
    assert "sslscan" in result["tasks"]
    assert "testssl" in result["tasks"]

def test_severity_mapper():
    assert SeverityMapper.map_severity("testssl", "CRITICAL") == SeverityEnum.high
    assert SeverityMapper.map_severity("nikto", "Medium") == SeverityEnum.medium
    assert SeverityMapper.map_severity("testssl", "LOW") == SeverityEnum.low
