import pytest
import os
from reconx.services.telemetry import TelemetryService
from reconx.services.health import HealthService
from reconx.services.backup import BackupService
from reconx.services.cache import CacheService
from reconx.services.configuration import ConfigurationService

def test_telemetry_service():
    payload = TelemetryService.log_event("api", "request_handled", {"latency": 15})
    assert payload["service"] == "api"
    assert payload["event"] == "request_handled"
    assert payload["metrics"]["latency"] == 15
    assert "timestamp" in payload

def test_health_service():
    health = HealthService.check_health()
    assert health["status"] == "healthy"
    assert health["components"]["database"] == "up"

    ready = HealthService.check_ready()
    assert ready["ready"] == True

def test_backup_service():
    result = BackupService.initiate_database_backup()
    assert "Backup initiated" in result

def test_cache_service():
    cache = CacheService()
    cache.set("asset_1", {"ip": "1.1.1.1"})
    val = cache.get("asset_1")
    assert val is not None
    assert val["ip"] == "1.1.1.1"
    assert cache.get("missing") is None

def test_configuration_service(monkeypatch):
    # Test base fallback
    config = ConfigurationService.load_config()
    assert config["log_level"] == "INFO"

    # Test environment variable override
    monkeypatch.setenv("RECONX_LOG_LEVEL", "DEBUG")
    config_overriden = ConfigurationService.load_config()
    assert config_overriden["log_level"] == "DEBUG"
