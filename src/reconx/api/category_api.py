import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class CategoryAPI:
    def handle_request(self, method, path):
        parts = path.strip("/").split("/")
        if len(parts) >= 2 and parts[0] == "api" and parts[1] == "categories":
            if len(parts) == 2 and method == "GET":
                return {
                    "categories": [
                        "Recon & Info",
                        "Web",
                        "Vulnerability",
                        "Cloud",
                        "OSINT",
                        "Screenshot",
                        "Secrets",
                    ]
                }
            if len(parts) == 4 and parts[3] == "run" and method == "POST":
                return {"status": "category_started"}
        return {"error": "Invalid category endpoint"}
