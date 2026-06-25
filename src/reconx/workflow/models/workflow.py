from datetime import datetime, timezone
from typing import Any

from pydantic import BaseModel, Field

from reconx.state.models import TaskStatus, WorkflowState


class WorkflowTask(BaseModel):
    id: str
    plugin: str
    depends_on: list[str] = []
    timeout: int = 300
    retries: int = 3


class Workflow(BaseModel):
    id: str
    name: str
    tasks: list[WorkflowTask]


class TaskExecutionState(BaseModel):
    task_id: str
    plugin: str
    status: TaskStatus = TaskStatus.PENDING
    start_time: datetime | None = None
    end_time: datetime | None = None
    retries_used: int = 0
    error: str | None = None
    result: dict[str, Any] | None = None


class WorkflowExecution(BaseModel):
    workflow_id: str
    target: str
    status: WorkflowState = WorkflowState.PENDING
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    started_at: datetime | None = None
    completed_at: datetime | None = None
    tasks: dict[str, TaskExecutionState] = {}
