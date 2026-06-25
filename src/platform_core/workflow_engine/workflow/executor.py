import asyncio
import datetime

from data.database.session import async_session_factory
from core.events.bus import event_bus
from core.events.models import TaskEvent
from core.logging.logger import setup_logger
from platform_core.plugin_engine.manager import plugin_manager
from platform_core.orchestration.state.models import TaskStatus
from platform_core.workflow_engine.workflow.execution_context import ExecutionContext
from platform_core.workflow_engine.workflow.models.workflow import TaskExecutionState, WorkflowTask

logger = setup_logger("TaskExecutor")


class TaskExecutor:
    @staticmethod
    async def execute(task: WorkflowTask, context: ExecutionContext, state: TaskExecutionState):
        state.status = TaskStatus.RUNNING
        state.start_time = datetime.datetime.now(datetime.timezone.utc)
        await event_bus.publish(
            TaskEvent(
                event_id=task.id,
                event_type="TaskStarted",
                correlation_id=context.workflow_id,
                source="executor",
                task_id=task.id,
            )
        )

        success = False
        while state.retries_used <= task.retries and not success:
            if state.status == TaskStatus.CANCELLED:
                break

            try:
                # Use wait_for on top of the plugin manager execution
                async with async_session_factory():
                    coro = plugin_manager.execute(task.plugin, context.target)
                    result = await asyncio.wait_for(coro, timeout=task.timeout)

                if result.success:
                    success = True
                    state.status = TaskStatus.SUCCESS
                    state.result = result.model_dump()
                    await event_bus.publish(
                        TaskEvent(
                            event_id=task.id,
                            event_type="TaskCompleted",
                            correlation_id=context.workflow_id,
                            source="executor",
                            task_id=task.id,
                            payload={"result": "success"},
                        )
                    )
                else:
                    state.retries_used += 1
                    error_msg = f"Plugin returned errors: {result.errors}"
                    if state.retries_used > task.retries:
                        state.status = TaskStatus.FAILED
                        state.error = error_msg
                        await event_bus.publish(
                            TaskEvent(
                                event_id=task.id,
                                event_type="TaskFailed",
                                correlation_id=context.workflow_id,
                                source="executor",
                                task_id=task.id,
                                payload={"error": state.error},
                            )
                        )
                    else:
                        logger.warning(
                            f"Task {task.id} failed, retrying... ({state.retries_used}/{task.retries})"
                        )

            except asyncio.TimeoutError:
                state.retries_used += 1
                error_msg = f"Task timed out after {task.timeout}s"
                if state.retries_used > task.retries:
                    state.status = TaskStatus.FAILED
                    state.error = error_msg
                    await event_bus.publish(
                        TaskEvent(
                            event_id=task.id,
                            event_type="TaskFailed",
                            correlation_id=context.workflow_id,
                            source="executor",
                            task_id=task.id,
                            payload={"error": state.error},
                        )
                    )
            except asyncio.CancelledError:
                state.status = TaskStatus.CANCELLED
                await event_bus.publish(
                    TaskEvent(
                        event_id=task.id,
                        event_type="TaskCancelled",
                        correlation_id=context.workflow_id,
                        source="executor",
                        task_id=task.id,
                    )
                )
                raise
            except Exception as e:
                state.retries_used += 1
                if state.retries_used > task.retries:
                    state.status = TaskStatus.FAILED
                    state.error = str(e)
                    await event_bus.publish(
                        TaskEvent(
                            event_id=task.id,
                            event_type="TaskFailed",
                            correlation_id=context.workflow_id,
                            source="executor",
                            task_id=task.id,
                            payload={"error": state.error},
                        )
                    )

        state.end_time = datetime.datetime.now(datetime.timezone.utc)
