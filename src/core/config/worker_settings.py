import os

from pydantic_settings import BaseSettings


class WorkerSettings(BaseSettings):
    """
    Configuration for globally distributed worker nodes.
    """

    # The geographic region this worker is deployed in (e.g., us-east-1, eu-central-1)
    # Used by the Orchestrator to route region-specific tasks.
    region: str = os.environ.get("RECONX_WORKER_REGION", "global")

    # Concurrency limit for this specific worker instance
    max_concurrent_tasks: int = int(os.environ.get("RECONX_MAX_TASKS", "10"))

    # Whether this worker should accept 'heavy' tasks like browser rendering
    accepts_heavy_loads: bool = os.environ.get("RECONX_HEAVY_WORKER", "false").lower() == "true"


worker_settings = WorkerSettings()
