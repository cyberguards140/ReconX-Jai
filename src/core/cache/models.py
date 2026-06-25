from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class CacheEntry(BaseModel):
    key: str
    value: Any
    expires_at: datetime | None = None


class SessionData(BaseModel):
    session_id: str
    user_id: str
    role: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    expires_at: datetime
    metadata: dict[str, Any] = Field(default_factory=dict)


class RateLimitRecord(BaseModel):
    identifier: str
    endpoint: str
    hits: int
    window_start: datetime


class TaskQueueItem(BaseModel):
    task_id: str
    queue_name: str
    payload: dict[str, Any]
    enqueued_at: datetime = Field(default_factory=datetime.utcnow)
