import pytest
import os
import json
from reconx.modules.reporting.evidence_manager import EvidenceManager
from reconx.modules.reporting.export_engine import ExportEngine
from reconx.modules.reporting.report_engine import ReportEngine

def test_evidence_manager():
    manager = EvidenceManager(storage_dir="/tmp/test_reconx_evidence")
    manager.store_evidence("finding_123", "Nmap Output: Ports 80, 443 open")
    content = manager.get_evidence("finding_123")
    assert "Nmap Output" in content
    
    # Cleanup
    os.remove("/tmp/test_reconx_evidence/finding_123.txt")

def test_export_engine_json():
    data = {"test": 123, "string": "value"}
    json_output = ExportEngine.export_json(data)
    parsed = json.loads(json_output)
    assert parsed["test"] == 123

def test_export_engine_csv():
    headers = ["h1", "h2"]
    rows = [["a", "b"], ["c", "d"]]
    csv_output = ExportEngine.export_csv(headers, rows)
    assert "h1,h2" in csv_output
    assert "a,b" in csv_output

def test_export_engine_html():
    html_output = ExportEngine.export_html("Test Title", "<p>Body</p>")
    assert "Test Title" in html_output
    assert "<p>Body</p>" in html_output

def test_report_engine_executive():
    report = ReportEngine.generate_executive_summary(asset_count=100, critical_count=5, high_count=10)
    assert report["type"] == "executive"
    assert report["risk_summary"]["critical"] == 5
    assert report["risk_summary"]["high"] == 10

def test_report_engine_technical():
    report = ReportEngine.generate_technical_report([{"title": "Vuln 1"}, {"title": "Vuln 2"}])
    assert report["type"] == "technical"
    assert report["findings_count"] == 2
    assert len(report["findings"]) == 2
