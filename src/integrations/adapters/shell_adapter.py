class ShellAdapter:
    def __init__(self, process_runner):
        self.runner = process_runner

    def execute(self, job_id, command):
        # Wraps execution via shell
        self.runner.run(job_id, command)
