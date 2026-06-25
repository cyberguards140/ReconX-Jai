from typing import Any

from fastapi import APIRouter, Depends, HTTPException

from reconx.api.dependencies import get_current_user
from reconx.workflow.engine.workflow_engine import WorkflowEngine
from reconx.workflow.playbooks.playbook_engine import PlaybookEngine
from reconx.workflow.scheduler.job_manager import JobManager

router = APIRouter(prefix="/workflow", tags=["Workflow Automation"])
workflow_engine = WorkflowEngine()
playbook_engine = PlaybookEngine()


@router.on_event("startup")
async def startup_event():
    """Sync built-in playbooks and setup scheduler on startup."""
    await playbook_engine.sync_builtin_playbooks()
    JobManager.setup_beat_schedule()


@router.get("/playbooks", response_model=list[dict[str, Any]])
async def list_playbooks(current_user: Any = Depends(get_current_user)):
    """List all available SOAR playbooks and workflow templates."""
    return await playbook_engine.get_all_playbooks()


@router.post("/execute/{workflow_name}")
async def execute_workflow(
    workflow_name: str, payload: dict[str, Any], current_user: Any = Depends(get_current_user)
):
    """Trigger a workflow execution by name."""
    try:
        # Pass the user's tenant if applicable
        tenant_id = getattr(current_user, "tenant_id", None)
        execution_id = await workflow_engine.trigger_workflow(workflow_name, payload, tenant_id)
        return {
            "status": "success",
            "execution_id": execution_id,
            "message": "Workflow execution queued.",
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/execution/{execution_id}")
async def get_execution_status(execution_id: str, current_user: Any = Depends(get_current_user)):
    """Get the status of a specific workflow execution."""
    status = await workflow_engine.get_execution_status(execution_id)
    if not status:
        raise HTTPException(status_code=404, detail="Execution not found.")
    return status


@router.post("/jobs/trigger/{job_type}")
async def trigger_ad_hoc_job(
    job_type: str, payload: dict[str, Any], current_user: Any = Depends(get_current_user)
):
    """Trigger an ad-hoc system job via Celery."""
    try:
        task = JobManager.trigger_ad_hoc_job(job_type, payload)
        return {"status": "success", "task_id": task.id, "message": "Job queued."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
