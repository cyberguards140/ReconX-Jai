from pydantic import BaseModel, Field
from datetime import datetime
from typing import Dict, Any, Optional

class CacheEntry(BaseModel):
    key: str
    value: Any
    expires_at: Optional[datetime] = None

class SessionData(BaseModel):
    session_id: str
    user_id: str
    role: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    expires_at: datetime
    metadata: Dict[str, Any] = Field(default_factory=dict)

class RateLimitRecord(BaseModel):
    identifier: str
    endpoint: str
    hits: int
    window_start: datetime

class TaskQueueItem(BaseModel):
    task_id: str
    queue_name: str
    payload: Dict[str, Any]
    enqueued_at: datetime = Field(default_factory=datetime.utcnow)
