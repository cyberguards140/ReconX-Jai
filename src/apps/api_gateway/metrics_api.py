import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class MetricsAPI:
    def handle_request(self, method, path):
        parts = path.strip("/").split("/")
        if len(parts) >= 2 and parts[0] == "api" and parts[1] == "metrics":
            return {"metrics": "active"}
        return {"error": "Invalid metrics endpoint"}
