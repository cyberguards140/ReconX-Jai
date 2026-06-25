import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class PipelineAPI:
    def handle_request(self, method, path):
        parts = path.strip("/").split("/")
        if len(parts) >= 2 and parts[0] == "api" and parts[1] == "pipelines":
            if len(parts) == 2 and method == "GET":
                return {"pipelines": ["Quick Recon", "Full ASM"]}
            if len(parts) == 4 and parts[3] == "run" and method == "POST":
                return {"status": "pipeline_started"}
        return {"error": "Invalid pipeline endpoint"}
