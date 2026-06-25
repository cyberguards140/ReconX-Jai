import re
import uuid
from datetime import datetime, timezone
from typing import Any

from recon.modules.asm_core.schema import UnifiedAsset


class NormalizationEngine:
    def __init__(self):
        pass

    def detect_type(self, value: str) -> str:
        """Heuristic detection of asset type."""
        value = value.strip().lower()
        if value.startswith("http://") or value.startswith("https://"):
            if value.count("/") > 2:
                return "url"
            else:
                return "service"
        if re.match(r"^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+$", value):
            return "ip"
        if re.match(r"^[a-zA-Z0-9-]+\.[a-zA-Z]{2,}$", value):
            return "domain"
        if "." in value and value.count(".") >= 2:
            return "subdomain"
        if value.startswith("/"):
            return "endpoint"

        return "unknown"

    def normalize(self, raw_data: dict[str, Any], source: str) -> UnifiedAsset:
        """Normalize a raw dictionary into a UnifiedAsset."""
        value = (
            raw_data.get("value")
            or raw_data.get("host")
            or raw_data.get("ip")
            or raw_data.get("url", "")
        )
        value = str(value).strip()

        asset_type = raw_data.get("asset_type") or self.detect_type(value)
        asset_id = str(uuid.uuid4())

        confidence = float(raw_data.get("confidence", 50.0))

        metadata = raw_data.get("metadata", {})
        if not metadata:
            metadata = {
                "dns": raw_data.get("dns", {}),
                "http": raw_data.get("http", {}),
                "tech": raw_data.get("tech", []),
                "geo": raw_data.get("geo", {}),
            }

        return UnifiedAsset(
            asset_id=asset_id,
            asset_type=asset_type,
            value=value,
            source=source,
            confidence=confidence,
            metadata=metadata,
            timestamp=datetime.now(timezone.utc),
        )
