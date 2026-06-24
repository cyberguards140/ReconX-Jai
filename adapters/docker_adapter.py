class DockerAdapter:
    def __init__(self, process_runner):
        self.runner = process_runner
        
    def execute(self, job_id, command):
        # Prefix with docker run...
        docker_cmd = f"docker run --rm {command}"
        self.runner.run(job_id, docker_cmd)
