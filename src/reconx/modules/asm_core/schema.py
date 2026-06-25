from pydantic import BaseModel, Field
from typing import Dict, List, Any, Optional
from datetime import datetime, timezone

class UnifiedAsset(BaseModel):
    asset_id: str
    asset_type: str  # domain | subdomain | ip | url | endpoint | service
    value: str
    source: str
    confidence: float = 0.0
    metadata: Dict[str, Any] = Field(default_factory=lambda: {"dns": {}, "http": {}, "tech": [], "geo": {}})
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class ValidationSignal(BaseModel):
    asset_id: str
    status: str  # alive | dead | unknown
    signals: List[Dict[str, Any]] = Field(default_factory=list)
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
