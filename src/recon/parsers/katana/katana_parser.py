import json
from core.models.asset import ReconAsset

class KatanaParser:
    """
    Parses Katana crawler JSON output.
    """
    def parse(self, json_line: str) -> ReconAsset:
        try:
            data = json.loads(json_line)
        except json.JSONDecodeError:
            return None

        url = data.get("request", {}).get("endpoint") or data.get("url")
        if not url:
            return None

        method = data.get("request", {}).get("method", "GET")
        
        return ReconAsset(
            asset_type="endpoint",
            value=url,
            sources=["Katana"],
            confidence=1.0,
            metadata={"method": method}
        )
