import glob
import os
from typing import List, Optional, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from reconx.workflow.workflow_engine import workflow_engine
from reconx.state.manager import StateManager
from reconx.database.session import async_session_factory
from reconx.logger import setup_logger

logger = setup_logger("WorkflowService")

class WorkflowService:
    def __init__(self, db_session: Optional[AsyncSession] = None):
        self.db_session = db_session

    async def list_workflows(self) -> List[str]:
        workflows = []
        for f in glob.glob("src/reconx/workflows/*.yaml"):
            workflows.append(os.path.basename(f).replace(".yaml", ""))
        return workflows

    async def start_workflow(self, name: str, target: str, user_id: Optional[str] = None) -> Dict[str, Any]:
        return await workflow_engine.execute_workflow(name, target, user_id)

    async def get_workflow(self, execution_id: str) -> Optional[Any]:
        if self.db_session:
            state_manager = StateManager(self.db_session)
            return await state_manager.get_execution(execution_id)
        
        async with async_session_factory() as db:
            state_manager = StateManager(db)
            return await state_manager.get_execution(execution_id)

    async def cancel_workflow(self, execution_id: str) -> bool:
        if self.db_session:
            state_manager = StateManager(self.db_session)
            record = await state_manager.get_execution(execution_id)
            if not record or record.status in ["completed", "failed", "cancelled"]:
                return False
            workflow_engine.cancel_workflow(execution_id)
            await state_manager.update_status(execution_id, "CANCELLED")
            return True
        
        async with async_session_factory() as db:
            state_manager = StateManager(db)
            record = await state_manager.get_execution(execution_id)
            if not record or record.status in ["completed", "failed", "cancelled"]:
                return False
            workflow_engine.cancel_workflow(execution_id)
            await state_manager.update_status(execution_id, "CANCELLED")
            return True

# Singleton for convenience in non-DI contexts (CLI)
workflow_service = WorkflowService()
