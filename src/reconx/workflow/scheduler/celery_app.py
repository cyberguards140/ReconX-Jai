import os
from celery import Celery
from celery.schedules import crontab

# Configure Celery with Redis backend and broker. 
# Uses environment variables with sensible defaults for local dev.
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

celery_app = Celery(
    "reconx_workflows",
    broker=REDIS_URL,
    backend=REDIS_URL,
    include=[
        "reconx.workflow.queue.task_queue"
    ]
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=3600, # Max 1 hour
    worker_prefetch_multiplier=1,
)

# Optional: configure periodic tasks directly in celery if needed, or rely on beat_scheduler.py
celery_app.conf.beat_schedule = {
    # 'daily-recon-sync': {
    #     'task': 'reconx.workflow.queue.task_queue.run_recon_sync',
    #     'schedule': crontab(minute=0, hour=0),
    # },
}
