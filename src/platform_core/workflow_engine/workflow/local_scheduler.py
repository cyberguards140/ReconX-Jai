import asyncio

from core.logging.logger import setup_logger
from platform_core.orchestration.state.models import TaskStatus
from platform_core.workflow_engine.workflow.dependency_graph import DependencyGraph
from platform_core.workflow_engine.workflow.execution_context import ExecutionContext
from platform_core.workflow_engine.workflow.executor import TaskExecutor
from platform_core.workflow_engine.workflow.models.workflow import WorkflowExecution, WorkflowTask
from platform_core.workflow_engine.workflow.result_aggregator import ResultAggregator

logger = setup_logger("WorkflowScheduler")


class WorkflowScheduler:
    def __init__(
        self,
        execution: WorkflowExecution,
        graph: DependencyGraph,
        context: ExecutionContext,
        aggregator: ResultAggregator,
    ):
        self.execution = execution
        self.graph = graph
        self.context = context
        self.aggregator = aggregator

        self.completed = set()
        self.failed = set()
        self.running_tasks = set()
        self.active_async_tasks = set()
        self._cancelled = False

    def cancel_workflow(self):
        self._cancelled = True
        for t in self.active_async_tasks:
            t.cancel()

    async def schedule_task(self, task: WorkflowTask):
        state = self.execution.tasks[task.id]
        if self._cancelled:
            state.status = TaskStatus.CANCELLED
            self.failed.add(task.id)
            return

        try:
            await TaskExecutor.execute(task, self.context, state)
        except asyncio.CancelledError:
            self._cancelled = True
            state.status = TaskStatus.CANCELLED
            self.failed.add(task.id)
            raise
        finally:
            self.running_tasks.remove(task.id)
            if state.status == TaskStatus.SUCCESS:
                self.completed.add(task.id)
                # Parse results back into aggregator
                if state.result:
                    from platform_core.plugin_engine.schemas.plugin import PluginResult

                    await self.aggregator.add_result(task.id, PluginResult(**state.result))
            else:
                self.failed.add(task.id)

    async def run(self):
        try:
            total_tasks = len(self.graph.tasks)
            while len(self.completed) + len(self.failed) < total_tasks:
                if self._cancelled:
                    break

                # Mark skipped tasks
                skipped = self.graph.get_skipped_tasks(self.failed, self.completed)
                for s in skipped:
                    if s not in self.failed:
                        self.execution.tasks[s].status = TaskStatus.SKIPPED
                        self.failed.add(s)

                ready_tasks = self.graph.get_ready_tasks(
                    self.completed, self.failed, self.running_tasks
                )

                tasks_to_schedule = []
                for t in ready_tasks:
                    self.running_tasks.add(t.id)
                    task_coro = asyncio.create_task(self.schedule_task(t))
                    self.active_async_tasks.add(task_coro)
                    task_coro.add_done_callback(self.active_async_tasks.discard)
                    tasks_to_schedule.append(task_coro)

                if not tasks_to_schedule and self.running_tasks:
                    # Wait for running tasks
                    await asyncio.sleep(0.1)
                    continue
                elif not tasks_to_schedule and not self.running_tasks:
                    # Deadlock or done
                    break

            # If loop finishes and tasks are not all successful, the workflow technically didn't succeed entirely.
        except asyncio.CancelledError:
            self._cancelled = True
            raise
