from reconx.database.models import WorkflowExecution
from reconx.database.repositories.base import BaseRepository


class WorkflowExecutionRepository(BaseRepository[WorkflowExecution]):
    pass


workflow_execution_repo = WorkflowExecutionRepository(WorkflowExecution)
