from typing import Any

API_VERSIONS: dict[str, dict[str, Any]] = {
    "v1": {"status": "active", "deprecated": False, "description": "Stable V1 API"},
    "v2": {"status": "beta", "deprecated": False, "description": "Upcoming V2 API"},
}


class VersioningConfig:
    default_version = "v1"
    supported_versions = list(API_VERSIONS.keys())
