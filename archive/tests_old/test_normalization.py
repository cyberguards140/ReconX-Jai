import pytest
import asyncio
from typing import Any
from reconx.core.parsers.tool_parsers import NmapParser, AmassParser, NiktoParser
from reconx.core.normalizers.tool_normalizers import NmapNormalizer, AmassNormalizer, NiktoNormalizer
from reconx.core.asset_resolver import AssetResolver
from reconx.core.deduplication import DeduplicationEngine
from reconx.schemas.normalization import SeverityEnum

def test_nmap_normalization():
    raw = "some raw xml saying open port 80"
    parser = NmapParser()
    parsed = parser.parse(raw)
    
    assert len(parsed["hosts"]) == 1
    
    normalizer = NmapNormalizer()
    record = normalizer.normalize(parsed)
    
    assert record.asset.asset_type == "ip"
    assert record.asset.value == "127.0.0.1"
    assert len(record.ports) == 1
    assert record.ports[0].port == 80

def test_amass_normalization():
    raw = '{"name": "test.com"}\n{"name": "sub.test.com"}'
    parser = AmassParser()
    parsed = parser.parse(raw)
    
    assert len(parsed) == 2
    
    normalizer = AmassNormalizer()
    record = normalizer.normalize(parsed)
    
    assert record.asset.asset_type == "domain"
    assert record.asset.value == "test.com"

def test_nikto_normalization():
    raw = "OSVDB: vulnerability found\nfinding: another issue"
    parser = NiktoParser()
    parsed = parser.parse(raw)
    
    normalizer = NiktoNormalizer()
    record = normalizer.normalize(parsed)
    
    assert len(record.findings) == 2
    assert record.findings[0].severity == SeverityEnum.medium

def test_asset_resolver():
    a_type, a_val = AssetResolver.resolve("unknown", "http://192.168.1.1:8080/")
    assert a_type == "ip"
    assert a_val == "192.168.1.1"

    a_type, a_val = AssetResolver.resolve("host", "example.com")
    assert a_type == "domain"
    assert a_val == "example.com"

def test_deduplication():
    engine = DeduplicationEngine()
    
    assert not engine.is_duplicate_asset("proj1", "ip", "10.0.0.1")
    assert engine.is_duplicate_asset("proj1", "ip", "10.0.0.1")
    assert not engine.is_duplicate_asset("proj2", "ip", "10.0.0.1")
