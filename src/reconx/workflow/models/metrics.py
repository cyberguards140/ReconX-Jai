from pydantic import BaseModel

class WorkflowMetrics(BaseModel):
    workflow_id: str
    workflow_duration: float = 0.0
    task_duration_avg: float = 0.0
    success_rate: float = 0.0
    failure_rate: float = 0.0
    total_tasks: int = 0
    completed_tasks: int = 0
    failed_tasks: int = 0
