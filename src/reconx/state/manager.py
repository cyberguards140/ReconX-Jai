import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from reconx.database.models import WorkflowExecution as DBWorkflowExecution
from reconx.database.repositories.workflow_execution import workflow_execution_repo
from reconx.state.models import WorkflowState


class StateManager:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_execution(self, name: str, target: str, user_id: str) -> DBWorkflowExecution:
        exec_record = await workflow_execution_repo.create(
            self.db,
            obj_in={
                "workflow_name": name,
                "target": target,
                "user_id": user_id,
                "status": WorkflowState.PENDING.value,
                "started_at": datetime.datetime.now(datetime.timezone.utc),
            },
        )
        await self.db.flush()
        return exec_record

    async def update_status(self, exec_id: str, status: str, result_summary: str | None = None):
        record = await workflow_execution_repo.get(self.db, exec_id)
        if record:
            updates = {"status": status}
            if result_summary:
                updates["result_summary"] = result_summary
            if status in [
                WorkflowState.COMPLETED.value,
                WorkflowState.FAILED.value,
                WorkflowState.CANCELLED.value,
            ]:
                updates["finished_at"] = datetime.datetime.now(datetime.timezone.utc)
            await workflow_execution_repo.update(self.db, db_obj=record, obj_in=updates)
            await self.db.flush()

    async def get_execution(self, exec_id: str) -> DBWorkflowExecution | None:
        return await workflow_execution_repo.get(self.db, exec_id)
