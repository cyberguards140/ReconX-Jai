import os
from datetime import datetime

LOG_DIR_BASE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "projects")


class LogWriter:
    def __init__(self, project_name, job_id):
        self.project_name = project_name
        self.job_id = job_id
        self.log_dir = os.path.join(LOG_DIR_BASE, project_name, "logs", job_id)
        os.makedirs(self.log_dir, exist_ok=True)

        self.stdout_path = os.path.join(self.log_dir, "stdout.log")
        self.stderr_path = os.path.join(self.log_dir, "stderr.log")
        self.runtime_path = os.path.join(self.log_dir, "runtime.log")

    def write_stdout(self, line):
        with open(self.stdout_path, "a") as f:
            f.write(line + "\n")

    def write_stderr(self, line):
        with open(self.stderr_path, "a") as f:
            f.write(line + "\n")

    def write_runtime(self, message):
        now = datetime.now().isoformat()
        with open(self.runtime_path, "a") as f:
            f.write(f"[{now}] {message}\n")
