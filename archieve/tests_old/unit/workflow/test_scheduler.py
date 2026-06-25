import pytest
import pytest_asyncio
import asyncio
from reconx.workflow.models.workflow import WorkflowTask, WorkflowExecution, TaskExecutionState
from reconx.state.models import TaskStatus, WorkflowState
from reconx.workflow.dependency_graph import DependencyGraph
from reconx.workflow.scheduler import WorkflowScheduler
from reconx.workflow.execution_context import ExecutionContext
from reconx.workflow.result_aggregator import ResultAggregator

from reconx.workflow.executor import TaskExecutor

@pytest.mark.asyncio
async def test_scheduler_success():
    # Mock executor
    async def mock_execute(task, context, state):
        state.status = TaskStatus.SUCCESS
        state.result = {"plugin": task.plugin, "success": True, "execution_time": 0.1, "output": {}, "errors": [], "assets": [], "findings": []}

    original_execute = TaskExecutor.execute
    TaskExecutor.execute = mock_execute

    try:
        tasks = [
            WorkflowTask(id="A", plugin="test"),
            WorkflowTask(id="B", plugin="test", depends_on=["A"])
        ]
        graph = DependencyGraph(tasks)
        execution = WorkflowExecution(workflow_id="test", target="example.com")
        for t in tasks:
            execution.tasks[t.id] = TaskExecutionState(task_id=t.id, plugin=t.plugin)
            
        scheduler = WorkflowScheduler(
            execution, graph, ExecutionContext(workflow_id="test", target="example.com", user="test"), ResultAggregator()
        )
        await scheduler.run()

        assert "A" in scheduler.completed
        assert "B" in scheduler.completed
    finally:
        TaskExecutor.execute = original_execute


@pytest.mark.asyncio
async def test_scheduler_failure_and_skip():
    # Mock executor
    async def mock_execute(task, context, state):
        if task.id == "A":
            state.status = TaskStatus.FAILED
        else:
            state.status = TaskStatus.SUCCESS

    original_execute = TaskExecutor.execute
    TaskExecutor.execute = mock_execute

    try:
        tasks = [
            WorkflowTask(id="A", plugin="test"),
            WorkflowTask(id="B", plugin="test", depends_on=["A"])
        ]
        graph = DependencyGraph(tasks)
        execution = WorkflowExecution(workflow_id="test", target="example.com")
        for t in tasks:
            execution.tasks[t.id] = TaskExecutionState(task_id=t.id, plugin=t.plugin)
            
        scheduler = WorkflowScheduler(
            execution, graph, ExecutionContext(workflow_id="test", target="example.com", user="test"), ResultAggregator()
        )
        await scheduler.run()

        assert "A" in scheduler.failed
        assert "B" in scheduler.failed # Should be skipped, which counts as failed in scheduler sets
        assert execution.tasks["B"].status == TaskStatus.SKIPPED
    finally:
        TaskExecutor.execute = original_execute

@pytest.mark.asyncio
async def test_cancellation():
    async def mock_execute(task, context, state):
        state.status = TaskStatus.RUNNING
        try:
            await asyncio.sleep(2)
        except asyncio.CancelledError:
            state.status = TaskStatus.CANCELLED
            raise

    original_execute = TaskExecutor.execute
    TaskExecutor.execute = mock_execute

    try:
        tasks = [WorkflowTask(id="A", plugin="test")]
        graph = DependencyGraph(tasks)
        execution = WorkflowExecution(workflow_id="test", target="example.com")
        for t in tasks:
            execution.tasks[t.id] = TaskExecutionState(task_id=t.id, plugin=t.plugin)
            
        scheduler = WorkflowScheduler(
            execution, graph, ExecutionContext(workflow_id="test", target="example.com", user="test"), ResultAggregator()
        )
        
        run_task = asyncio.create_task(scheduler.run())
        await asyncio.sleep(0.1) # let it start
        scheduler.cancel_workflow()
        
        await run_task
            
        assert execution.tasks["A"].status == TaskStatus.CANCELLED
    finally:
        TaskExecutor.execute = original_execute
