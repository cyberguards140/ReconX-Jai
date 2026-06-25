import logging
from celery import shared_task
from typing import Dict, Any

logger = logging.getLogger(__name__)

@shared_task(bind=True, max_retries=3)
def execute_workflow_task(self, workflow_id: str, payload: Dict[str, Any]):
    """
    Executes a standard workflow by delegating back to the ExecutionEngine.
    """
    logger.info(f"Starting execution of workflow {workflow_id}")
    try:
        from reconx.workflow.engine.execution_engine import ExecutionEngine
        engine = ExecutionEngine()
        result = engine.run_workflow(workflow_id, payload)
        return {"status": "completed", "result": result}
    except Exception as exc:
        logger.error(f"Workflow {workflow_id} failed: {exc}")
        self.retry(exc=exc, countdown=2 ** self.request.retries)

@shared_task(bind=True)
def run_job(self, job_type: str, job_data: Dict[str, Any]):
    """
    Executes an ad-hoc system job (e.g. Graph Sync, Report).
    """
    logger.info(f"Executing job type: {job_type}")
    # In a real setup, dispatch to specific job handlers
    return {"status": "completed", "job_type": job_type}

@shared_task(bind=True)
def run_recon_sync(self):
    """
    Example periodic task for Recon sync.
    """
    logger.info("Running scheduled recon sync...")
    return {"status": "completed"}
