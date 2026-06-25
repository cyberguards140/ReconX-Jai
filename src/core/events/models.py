from datetime import datetime, timezone
from typing import Any

from pydantic import BaseModel, Field


class BaseEvent(BaseModel):
    event_id: str
    event_type: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    correlation_id: str
    source: str
    payload: dict[str, Any] = Field(default_factory=dict)


class WorkflowEvent(BaseEvent):
    pass


class TaskEvent(BaseEvent):
    task_id: str


class PluginEvent(BaseEvent):
    plugin_name: str


class ScanEvent(BaseEvent):
    scan_id: str
    target_id: str


class AssetEvent(BaseEvent):
    asset_id: str
    action: str


class FindingEvent(BaseEvent):
    finding_id: str
    severity: str


class AlertEvent(BaseEvent):
    alert_level: str
    message: str
