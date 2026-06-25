import datetime
from typing import Any


class ThreatCacheManager:
    """
    Optimizes performance by storing IOC matches and actor mappings.
    """

    def __init__(self):
        self._cache = {}

    def get_threat_data(self, asset_id: str) -> dict[str, Any] | None:
        record = self._cache.get(asset_id)
        if record:
            if record["expires_at"] > datetime.datetime.now(datetime.timezone.utc):
                return record["data"]
        return None

    def set_threat_data(self, asset_id: str, data: dict[str, Any], ttl_seconds: int = 3600):
        self._cache[asset_id] = {
            "data": data,
            "expires_at": datetime.datetime.now(datetime.timezone.utc)
            + datetime.timedelta(seconds=ttl_seconds),
        }
