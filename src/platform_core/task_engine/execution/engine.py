import logging
import os

from .adapter_manager import AdapterManager
from .job_tracker import JobTracker
from .process_runner import ProcessRunner

# from .queue_manager import QueueManager
# from .validator import Validator

LOG_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs")
os.makedirs(LOG_DIR, exist_ok=True)
logging.basicConfig(filename=os.path.join(LOG_DIR, "execution.log"), level=logging.INFO)


class ExecutionEngine:
    def __init__(self):
        self.job_tracker = JobTracker()
        self.process_runner = ProcessRunner(self.job_tracker)
        self.adapter_manager = AdapterManager(self.process_runner)

    def submit_job(self, request_data):
        tool = request_data.get("tool")
        project = request_data.get("project", "default")
        args = request_data.get("arguments", {})
        target = args.get("target", "")

        # 1. Create Job
        job_id = self.job_tracker.create_job(tool, project, target, args)

        # 2. Build Command
        from .command_builder import CommandBuilder
        import re
        
        command = CommandBuilder().build(tool, args)
        if target:
            if not re.match(r"^[a-zA-Z0-9\.\-\/:]+$", target) or target.startswith("-"):
                raise ValueError("Invalid target format")
            command.append(target)

        # 3. Route to Adapter
        # Read adapter type from registry, fallback to shell
        adapter = self.adapter_manager.get_adapter("shell_adapter")

        # 4. Enqueue & Execute (Synchronous for now)
        adapter.execute(job_id, command)

        return {"job_id": job_id, "status": "queued"}

    def get_job_status(self, job_id):
        return {"job_id": job_id, "status": self.job_tracker.get_job_status(job_id)}

    def cancel_job(self, job_id):
        self.job_tracker.update_status(job_id, "cancelled")
        return {"job_id": job_id, "status": "cancelled"}
