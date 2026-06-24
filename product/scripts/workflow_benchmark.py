import asyncio
import time
import uuid
import psutil
import os
from typing import List, Dict

from reconx.workflow.models.workflow import WorkflowTask, WorkflowExecution
from reconx.workflow.models.state import TaskStatus, WorkflowState
from reconx.workflow.dependency_graph import DependencyGraph
from reconx.workflow.scheduler import WorkflowScheduler
from reconx.workflow.result_aggregator import ResultAggregator
from reconx.workflow.execution_context import ExecutionContext

# Mock the executor for benchmarking
from reconx.workflow.executor import TaskExecutor

async def mock_execute(task: WorkflowTask, context: ExecutionContext, state):
    state.status = TaskStatus.RUNNING
    # simulate very fast execution
    await asyncio.sleep(0.001)
    state.status = TaskStatus.SUCCESS
    state.result = {"plugin": task.plugin, "success": True, "execution_time": 0.001, "output": {}, "errors": [], "assets": [], "findings": []}

TaskExecutor.execute = mock_execute

def generate_workflow(num_tasks: int) -> List[WorkflowTask]:
    tasks = []
    for i in range(num_tasks):
        deps = []
        if i > 0:
            # Randomly depend on previous tasks to create a complex DAG
            if i % 3 == 0:
                deps.append(f"task_{i-1}")
            if i % 5 == 0 and i > 5:
                deps.append(f"task_{i-5}")
        
        tasks.append(WorkflowTask(
            id=f"task_{i}",
            plugin="mock_plugin",
            depends_on=deps
        ))
    return tasks

async def run_benchmark(num_tasks: int):
    print(f"\n--- Benchmarking {num_tasks} Tasks ---")
    
    tasks = generate_workflow(num_tasks)
    graph = DependencyGraph(tasks)
    context = ExecutionContext(workflow_id="benchmark", target="example.com", user="test")
    aggregator = ResultAggregator()
    
    execution = WorkflowExecution(workflow_id="benchmark", target="example.com")
    for t in tasks:
        from reconx.workflow.models.workflow import TaskExecutionState
        execution.tasks[t.id] = TaskExecutionState(task_id=t.id, plugin=t.plugin)
    
    scheduler = WorkflowScheduler(execution, graph, context, aggregator)
    
    process = psutil.Process(os.getpid())
    mem_before = process.memory_info().rss / 1024 / 1024
    
    start_time = time.time()
    await scheduler.run()
    duration = time.time() - start_time
    
    mem_after = process.memory_info().rss / 1024 / 1024
    
    print(f"Execution Time: {duration:.4f} seconds")
    print(f"Memory Diff: {mem_after - mem_before:.2f} MB")
    print(f"Tasks Completed: {len(scheduler.completed)}")
    print(f"Tasks Failed: {len(scheduler.failed)}")
    
if __name__ == "__main__":
    asyncio.run(run_benchmark(10))
    asyncio.run(run_benchmark(100))
    asyncio.run(run_benchmark(1000))
