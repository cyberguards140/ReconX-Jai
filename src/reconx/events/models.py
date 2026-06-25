from datetime import datetime, timezone
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field

class BaseEvent(BaseModel):
    event_id: str
    event_type: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    correlation_id: str
    source: str
    payload: Dict[str, Any] = Field(default_factory=dict)

class WorkflowEvent(BaseEvent):
    pass

class TaskEvent(BaseEvent):
    task_id: str

class PluginEvent(BaseEvent):
    plugin_name: str
