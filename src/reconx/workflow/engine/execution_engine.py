import asyncio
import logging
from datetime import datetime, timezone
from typing import Any

from sqlalchemy import select

from reconx.database.models import SOARTaskExecution, SOARWorkflowExecution, SOARWorkflowTemplate
from reconx.database.session import async_session_factory
from reconx.workflow.engine.state_machine import TaskState, WorkflowState

logger = logging.getLogger(__name__)


class ExecutionEngine:
    """
    Executes a given SOAR workflow by coordinating its underlying tasks.
    Called by Celery worker processes.
    """

    def run_workflow(self, execution_id: str, payload: dict[str, Any]) -> dict[str, Any]:
        """
        Synchronous wrapper to run an async workflow execution.
        """
        try:
            return asyncio.run(self._run_workflow_async(execution_id, payload))
        except Exception as e:
            logger.error(f"Failed to execute workflow asynchronously: {e}")
            raise

    async def _run_workflow_async(
        self, execution_id: str, payload: dict[str, Any]
    ) -> dict[str, Any]:
        async with async_session_factory() as session:
            # 1. Fetch the execution record
            result = await session.execute(
                select(SOARWorkflowExecution).filter(SOARWorkflowExecution.id == execution_id)
            )
            execution = result.scalars().first()

            if not execution:
                raise ValueError(f"Workflow execution {execution_id} not found.")

            # Update State to RUNNING
            execution.status = WorkflowState.RUNNING.value
            execution.start_time = datetime.now(timezone.utc)
            await session.commit()

            # 2. Fetch the template
            result = await session.execute(
                select(SOARWorkflowTemplate).filter(
                    SOARWorkflowTemplate.id == execution.workflow_id
                )
            )
            template = result.scalars().first()

            if not template:
                execution.status = WorkflowState.FAILED.value
                execution.end_time = datetime.now(timezone.utc)
                execution.logs = [{"level": "error", "msg": "Template not found"}]
                await session.commit()
                raise ValueError("Workflow template not found.")

            definition = template.definition_json
            tasks_def = definition.get("tasks", [])

            logs = []

            try:
                # Naive sequential execution of tasks for the Engine
                for task_def in tasks_def:
                    task_name = task_def.get("name", "Unknown Task")
                    action = task_def.get("action", "noop")

                    # Create Task Execution Record
                    task_exec = SOARTaskExecution(
                        id=f"task-{execution_id}-{task_name}",
                        execution_id=execution.id,
                        celery_task_id="local",
                        task_name=task_name,
                        status=TaskState.RUNNING.value,
                    )
                    session.add(task_exec)
                    await session.commit()

                    # Execute task action (mocked or routed to plugins)
                    logger.info(f"Executing task: {task_name} (Action: {action})")
                    logs.append({"task": task_name, "status": "started", "action": action})

                    # Mock execution result
                    task_exec.status = TaskState.COMPLETED.value
                    task_exec.result = {"status": "success", "data": f"Executed {action}"}
                    session.add(task_exec)
                    await session.commit()

                    logs.append({"task": task_name, "status": "completed"})

                # Finalize Workflow
                execution.status = WorkflowState.COMPLETED.value
                execution.end_time = datetime.now(timezone.utc)
                execution.logs = logs
                await session.commit()
                return {"status": WorkflowState.COMPLETED.value, "logs": logs}

            except Exception as e:
                execution.status = WorkflowState.FAILED.value
                execution.end_time = datetime.now(timezone.utc)
                logs.append({"error": str(e)})
                execution.logs = logs
                await session.commit()
                raise e
