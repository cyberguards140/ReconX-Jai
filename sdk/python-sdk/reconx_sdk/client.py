import requests
from typing import Dict, Any, List

class ReconXClient:
    """
    Phase 61: ReconX Python SDK.
    Allows external developers to interact with the ReconX API programmatically.
    """
    def __init__(self, api_key: str, base_url: str = "http://localhost:8000/api/v1"):
        self.api_key = api_key
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({"Authorization": f"Bearer {self.api_key}"})

    def get_asset(self, asset_id: str) -> Dict[str, Any]:
        response = self.session.get(f"{self.base_url}/assets/{asset_id}")
        response.raise_for_status()
        return response.json()

    def trigger_scan(self, target: str, plugin_id: str) -> Dict[str, Any]:
        response = self.session.post(
            f"{self.base_url}/scans",
            json={"target": target, "plugin": plugin_id}
        )
        response.raise_for_status()
        return response.json()

    def get_macro_risk(self) -> Dict[str, Any]:
        """
        Retrieves the aggregated Global Risk Score and Cloud Exposure Index.
        """
        response = self.session.get(f"{self.base_url}/intelligence/risk")
        response.raise_for_status()
        return response.json()

    def trigger_autonomous_discovery(self, seed_target: str) -> Dict[str, Any]:
        """
        Kicks off the Phase 77 Autonomous Discovery Loop.
        """
        response = self.session.post(
            f"{self.base_url}/autonomous/start",
            json={"seed": seed_target}
        )
        response.raise_for_status()
        return response.json()
