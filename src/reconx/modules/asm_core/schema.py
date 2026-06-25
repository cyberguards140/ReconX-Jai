from datetime import datetime, timezone
from typing import Any

from pydantic import BaseModel, Field


class UnifiedAsset(BaseModel):
    asset_id: str
    asset_type: str  # domain | subdomain | ip | url | endpoint | service
    value: str
    source: str
    confidence: float = 0.0
    metadata: dict[str, Any] = Field(
        default_factory=lambda: {"dns": {}, "http": {}, "tech": [], "geo": {}}
    )
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class ValidationSignal(BaseModel):
    asset_id: str
    status: str  # alive | dead | unknown
    signals: list[dict[str, Any]] = Field(default_factory=list)
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
