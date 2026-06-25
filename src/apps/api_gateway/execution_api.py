import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from platform_core.task_engine.execution.engine import ExecutionEngine

engine = ExecutionEngine()


class ExecutionAPI:
    def handle_request(self, method, path, data=None):
        parts = path.strip("/").split("/")
        if len(parts) >= 3 and parts[0] == "api":
            # POST /api/tools/run
            if parts[1] == "tools" and parts[2] == "run" and method == "POST":
                return engine.submit_job(data or {})

            # Job endpoints
            if parts[1] == "jobs" and len(parts) >= 3:
                job_id = parts[2]

                # GET /api/jobs/{id}
                if len(parts) == 3 and method == "GET":
                    return engine.get_job_status(job_id)

                # POST /api/jobs/{id}/cancel
                if len(parts) == 4 and parts[3] == "cancel" and method == "POST":
                    return engine.cancel_job(job_id)

        return {"error": "Invalid execution endpoint"}
