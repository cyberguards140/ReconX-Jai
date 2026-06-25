import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class StreamingAPI:
    def handle_request(self, method, path):
        parts = path.strip("/").split("/")
        if len(parts) >= 3 and parts[0] == "api":
            # GET /api/jobs/{id}/status
            if len(parts) == 4 and parts[3] == "status" and method == "GET":
                return {"status": "streaming_engine_active"}

            # GET /api/jobs/{id}/logs
            if len(parts) == 4 and parts[3] == "logs" and method == "GET":
                return {"logs": "streaming_engine_active"}

            # GET /api/jobs/{id}/metrics
            if len(parts) == 4 and parts[3] == "metrics" and method == "GET":
                return {"metrics": "streaming_engine_active"}

        return {"error": "Invalid streaming endpoint"}
