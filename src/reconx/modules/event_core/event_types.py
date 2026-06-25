from pydantic import BaseModel, Field
from typing import Dict, Any, Optional
from datetime import datetime, timezone
import uuid

# Event Constants
ASSET_DISCOVERED = "ASSET_DISCOVERED"
ASSET_UPDATED = "ASSET_UPDATED"
ASSET_REMOVED = "ASSET_REMOVED"
INFRASTRUCTURE_CHANGED = "INFRASTRUCTURE_CHANGED"
NEW_ASN_DETECTED = "NEW_ASN_DETECTED"
NEW_NETBLOCK_DETECTED = "NEW_NETBLOCK_DETECTED"
CERTIFICATE_ISSUED = "CERTIFICATE_ISSUED"
NEW_ENDPOINT_FOUND = "NEW_ENDPOINT_FOUND"
NEW_SERVICE_DETECTED = "NEW_SERVICE_DETECTED"
RISK_SCORE_CHANGED = "RISK_SCORE_CHANGED"
RELATIONSHIP_CREATED = "RELATIONSHIP_CREATED"

class SystemEvent(BaseModel):
    event_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    event_type: str
    source: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    payload: Dict[str, Any] = Field(default_factory=dict)
    severity: str = "low"  # low | medium | high | critical
