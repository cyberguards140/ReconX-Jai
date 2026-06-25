from data.database.models import WorkflowExecution
from data.database.repositories.base import BaseRepository


class WorkflowExecutionRepository(BaseRepository[WorkflowExecution]):
    pass


workflow_execution_repo = WorkflowExecutionRepository(WorkflowExecution)
