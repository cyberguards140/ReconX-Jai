import uuid
import logging
from typing import Dict, Any, Optional
from datetime import datetime, timezone

from reconx.database.session import async_session_factory
from reconx.database.models import SOARWorkflowTemplate, SOARWorkflowExecution
from sqlalchemy import select
from reconx.workflow.queue.task_queue import execute_workflow_task
from reconx.workflow.engine.state_machine import WorkflowState

logger = logging.getLogger(__name__)

class WorkflowEngine:
    """
    Core engine for managing SOAR workflows.
    Responsible for creating execution records and queuing them to Celery.
    """

    async def trigger_workflow(self, workflow_name: str, payload: Dict[str, Any], tenant_id: Optional[str] = None) -> str:
        """
        Triggers a workflow by name and queues its execution via Celery.
        Returns the Execution ID.
        """
        async with async_session_factory() as session:
            # Look up the workflow template
            result = await session.execute(
                select(SOARWorkflowTemplate).filter(SOARWorkflowTemplate.name == workflow_name)
            )
            template = result.scalars().first()

            if not template:
                raise ValueError(f"Workflow template '{workflow_name}' not found.")

            # Create an execution record
            execution_id = str(uuid.uuid4())
            execution = SOARWorkflowExecution(
                id=execution_id,
                workflow_id=template.id,
                trigger_type="Manual",
                status=WorkflowState.QUEUED.value,
                tenant_id=tenant_id
            )
            session.add(execution)
            await session.commit()

            logger.info(f"Queued workflow execution {execution_id} for template {workflow_name}")

        # Queue the Celery Task
        execute_workflow_task.delay(execution_id, payload)

        return execution_id

    async def get_execution_status(self, execution_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieves the status and logs of a workflow execution.
        """
        async with async_session_factory() as session:
            result = await session.execute(
                select(SOARWorkflowExecution).filter(SOARWorkflowExecution.id == execution_id)
            )
            execution = result.scalars().first()

            if not execution:
                return None

            return {
                "execution_id": execution.id,
                "status": execution.status,
                "start_time": execution.start_time,
                "end_time": execution.end_time,
                "logs": execution.logs
            }
