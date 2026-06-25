import requests


class DashboardAPIMapper:
    """
    Translates Dashboard UI widget state into underlying API Gateway /api/v1/ calls.
    """

    def __init__(self, api_base="http://localhost:8000/api/v1"):
        self.api_base = api_base

    def get_attack_surface_stats(self, project_id: str):
        response = requests.get(
            f"{self.api_base}/analytics/attack-surface", params={"project_id": project_id}
        )
        return response.json() if response.status_code == 200 else {}

    def start_recon_pipeline(self, target: str):
        response = requests.post(f"{self.api_base}/scans/pipeline/start", json={"target": target})
        return response.json() if response.status_code == 200 else {}

    def fetch_assets(self, project_id: str, limit: int = 100):
        response = requests.get(
            f"{self.api_base}/assets/", params={"project_id": project_id, "limit": limit}
        )
        return response.json() if response.status_code == 200 else {}
