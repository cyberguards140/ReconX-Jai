import datetime
import json
from pathlib import Path
from typing import Any

import yaml

from reconx.config.settings import settings
from reconx.database.session import async_session_factory
from reconx.events.bus import event_bus
from reconx.events.models import WorkflowEvent
from reconx.logger import setup_logger
from reconx.state.manager import StateManager
from reconx.state.models import WorkflowState
from reconx.workflow.dependency_graph import DependencyGraph
from reconx.workflow.exceptions import WorkflowValidationError
from reconx.workflow.execution_context import ExecutionContext
from reconx.workflow.local_scheduler import WorkflowScheduler
from reconx.workflow.models.workflow import (
    TaskExecutionState,
    Workflow,
    WorkflowExecution,
    WorkflowTask,
)
from reconx.workflow.result_aggregator import ResultAggregator
from reconx.workflow.validator import WorkflowValidator

logger = setup_logger("WorkflowEngine")


class WorkflowEngine:
    def __init__(self, workflows_dir: str = None):
        self.workflows_dir = Path(workflows_dir or settings.workflow_directory)
        self.validator = WorkflowValidator()
        self.active_schedulers: dict[str, WorkflowScheduler] = {}

    def load_workflow(self, name: str) -> Workflow:
        if ".." in name or "/" in name or "\\" in name:
            raise WorkflowValidationError("Invalid workflow name")

        file_path = self.workflows_dir / f"{name}.yaml"
        if not file_path.exists():
            file_path = self.workflows_dir / "custom" / f"{name}.yaml"
            if not file_path.exists():
                raise WorkflowValidationError(f"Workflow {name} not found")

        with open(file_path, encoding="utf-8") as f:
            data = yaml.safe_load(f)

        self.validator.validate_workflow_def(data)

        tasks = [WorkflowTask(**t) for t in data["tasks"]]
        return Workflow(id=data.get("id", name), name=data["name"], tasks=tasks)

    def cancel_workflow(self, execution_id: str):
        if execution_id in self.active_schedulers:
            self.active_schedulers[execution_id].cancel_workflow()

    async def execute_workflow(
        self, name: str, target: str, user_id: str = "system"
    ) -> dict[str, Any]:
        workflow_def = self.load_workflow(name)
        graph = DependencyGraph(workflow_def.tasks)
        context = ExecutionContext(workflow_id=name, target=target, user=user_id)
        aggregator = ResultAggregator()

        # Build Execution State model
        execution = WorkflowExecution(workflow_id=name, target=target)
        for task in workflow_def.tasks:
            execution.tasks[task.id] = TaskExecutionState(task_id=task.id, plugin=task.plugin)

        async with async_session_factory() as db:
            state_manager = StateManager(db)
            exec_record = await state_manager.create_execution(name, target, user_id)
            execution_id = exec_record.id

            execution.started_at = datetime.datetime.now(datetime.timezone.utc)
            execution.status = WorkflowState.RUNNING
            await event_bus.publish(
                WorkflowEvent(
                    event_id=execution_id,
                    event_type="WorkflowStarted",
                    correlation_id=name,
                    source="workflow_engine",
                    payload={"target": target},
                )
            )

            scheduler = WorkflowScheduler(execution, graph, context, aggregator)
            self.active_schedulers[execution_id] = scheduler

            try:
                await scheduler.run()
            except Exception as e:
                execution.status = WorkflowState.FAILED
                await event_bus.publish(
                    WorkflowEvent(
                        event_id=execution_id,
                        event_type="WorkflowError",
                        correlation_id=name,
                        source="workflow_engine",
                        payload={"error": str(e)},
                    )
                )

            if execution_id in self.active_schedulers:
                del self.active_schedulers[execution_id]

            summary = aggregator.get_summary()

            # If ANY task failed, overall workflow is failed
            if scheduler._cancelled:
                execution.status = WorkflowState.CANCELLED
            elif scheduler.failed:
                execution.status = WorkflowState.FAILED
            else:
                execution.status = WorkflowState.COMPLETED

            execution.completed_at = datetime.datetime.now(datetime.timezone.utc)

            # Stage 2 Integration: Normalize and Ingest records via Canonical schema pipeline
            from reconx.core.pipeline import IngestionPipeline

            pipeline = IngestionPipeline(db)
            if aggregator.records:
                await pipeline.process(
                    project_id=settings.project_id, scan_id=execution_id, records=aggregator.records
                )

            # Stage 9 Integration (unchanged logic for legacy schemas if they exist)
            from reconx.services.intelligence.intelligence_store import IntelligenceStore

            intel_store = IntelligenceStore(db)
            await intel_store.ingest_plugin_result(
                project_id=settings.project_id,
                results={
                    "assets": summary.get("unique_assets", []),
                    "findings": aggregator.findings,
                },
            )

            await state_manager.update_status(
                execution_id, execution.status.value, json.dumps(summary)
            )

            event_type = (
                "WorkflowCompleted"
                if execution.status == WorkflowState.COMPLETED
                else "WorkflowFailed"
            )
            await event_bus.publish(
                WorkflowEvent(
                    event_id=execution_id,
                    event_type=event_type,
                    correlation_id=name,
                    source="workflow_engine",
                    payload={"target": target, "summary": summary},
                )
            )

            return {
                "execution_id": execution_id,
                "status": execution.status.value,
                "summary": summary,
                "tasks_completed": len(scheduler.completed),
                "tasks_failed": len(scheduler.failed),
            }


workflow_engine = WorkflowEngine()
