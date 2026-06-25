import threading
import time

from core.legacy_core.job_manager import JobManager
from core.legacy_core.process_manager import ProcessManager


class Scheduler:
    MAX_CONCURRENT = 5
    _running = False
    _thread = None

    @classmethod
    def start(cls):
        if cls._running:
            return
        cls._running = True
        cls._thread = threading.Thread(target=cls._loop, daemon=True)
        cls._thread.start()

    @classmethod
    def stop(cls):
        cls._running = False

    @classmethod
    def _loop(cls):
        while cls._running:
            running_jobs = JobManager.get_jobs_by_status("running")
            if len(running_jobs) < cls.MAX_CONCURRENT:
                queued_jobs = JobManager.get_jobs_by_status("queued")
                if queued_jobs:
                    job_to_run = queued_jobs[0]
                    # Update status instantly to prevent double launch
                    JobManager.update_status(job_to_run["id"], "running")

                    full_job = JobManager.get_job(job_to_run["id"])
                    ProcessManager.run_process(
                        job_id=full_job["id"],
                        tool_id=full_job["tool_id"],
                        command_string=full_job["command"],
                    )
            time.sleep(2)
