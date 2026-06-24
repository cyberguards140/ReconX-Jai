from typing import Dict, Any, Optional
import datetime
import uuid

class IntelligenceCache:
    """
    Abstract layer for storing and retrieving external intelligence lookups.
    """
    def __init__(self):
        self._in_memory_cache = {}

    def get_intel(self, lookup_key: str) -> Optional[Dict[str, Any]]:
        record = self._in_memory_cache.get(lookup_key)
        if record:
            # Check expiration structurally
            if record["expires_at"] > datetime.datetime.now(datetime.timezone.utc):
                return record["data"]
        return None

    def set_intel(self, lookup_key: str, data: Dict[str, Any], ttl_seconds: int = 3600):
        expires_at = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(seconds=ttl_seconds)
        self._in_memory_cache[lookup_key] = {
            "data": data,
            "expires_at": expires_at
        }
