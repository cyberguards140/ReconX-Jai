from reconx.database.repositories.base import BaseRepository
from reconx.database.models import WorkflowExecution

class WorkflowExecutionRepository(BaseRepository[WorkflowExecution]):
    pass

workflow_execution_repo = WorkflowExecutionRepository(WorkflowExecution)
