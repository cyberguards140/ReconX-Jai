import logging
from typing import Any

from celery.schedules import crontab

from platform_core.workflow_engine.workflow.scheduler.celery_app import celery_app

logger = logging.getLogger(__name__)


class JobManager:
    """
    Manages background jobs and scheduled tasks using Celery.
    """

    @staticmethod
    def setup_beat_schedule():
        """
        Configures the default recurring jobs for the ReconX platform.
        """
        celery_app.conf.beat_schedule = {
            "daily-recon-sync": {
                "task": "reconx.workflow.queue.task_queue.run_recon_sync",
                "schedule": crontab(hour=2, minute=0),  # Run daily at 2:00 AM
            },
        }
        logger.info("Celery beat schedules configured.")

    @staticmethod
    def trigger_ad_hoc_job(job_type: str, payload: dict[str, Any]):
        """
        Triggers an immediate ad-hoc job.
        """
        from platform_core.workflow_engine.workflow.queue.task_queue import run_job

        logger.info(f"Triggering ad-hoc job: {job_type}")
        return run_job.delay(job_type, payload)
