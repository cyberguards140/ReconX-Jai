class PythonAdapter:
    def __init__(self, process_runner):
        self.runner = process_runner

    def execute(self, job_id, command):
        # Prefix with python3
        py_cmd = f"python3 {command}"
        self.runner.run(job_id, py_cmd)
