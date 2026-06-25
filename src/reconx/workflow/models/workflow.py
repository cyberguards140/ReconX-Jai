from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime, timezone
from reconx.state.models import WorkflowState, TaskStatus

class WorkflowTask(BaseModel):
    id: str
    plugin: str
    depends_on: List[str] = []
    timeout: int = 300
    retries: int = 3

class Workflow(BaseModel):
    id: str
    name: str
    tasks: List[WorkflowTask]

class TaskExecutionState(BaseModel):
    task_id: str
    plugin: str
    status: TaskStatus = TaskStatus.PENDING
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    retries_used: int = 0
    error: Optional[str] = None
    result: Optional[Dict[str, Any]] = None

class WorkflowExecution(BaseModel):
    workflow_id: str
    target: str
    status: WorkflowState = WorkflowState.PENDING
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    tasks: Dict[str, TaskExecutionState] = {}
