from typing import Any

from recon.modules.asm_core.schema import UnifiedAsset


class CorrelationEngine:
    """
    Correlation engine to link assets.
    """

    def __init__(self):
        self.asset_cache = {}  # In-memory cache for correlation

    def add_to_cache(self, asset: UnifiedAsset):
        self.asset_cache[asset.asset_id] = asset

    def correlate(self, asset: UnifiedAsset) -> list[dict[str, Any]]:
        """
        Determine relationships for a given asset against the cache.
        Returns a list of relationship edges.
        """
        edges = []
        for cached_id, cached_asset in self.asset_cache.items():
            if cached_id == asset.asset_id:
                continue

            # Rule 1: same domain = BELONGS_TO
            if asset.asset_type == "subdomain" and cached_asset.asset_type == "domain":
                if asset.value.endswith(cached_asset.value):
                    edges.append(
                        {
                            "source": asset.asset_id,
                            "target": cached_id,
                            "relationship": "BELONGS_TO",
                        }
                    )

            # Rule 2: IP to Subdomain = RESOLVES_TO
            if asset.asset_type == "ip" and cached_asset.asset_type == "subdomain":
                # Assuming metadata contains resolution hints
                if asset.value in cached_asset.metadata.get("dns", {}).get("a_records", []):
                    edges.append(
                        {
                            "source": cached_id,
                            "target": asset.asset_id,
                            "relationship": "RESOLVES_TO",
                        }
                    )

            # Rule 3: Service to IP = HOSTS / RUNS_ON
            if asset.asset_type == "service" and cached_asset.asset_type == "ip":
                if cached_asset.value in asset.value:
                    edges.append(
                        {"source": cached_id, "target": asset.asset_id, "relationship": "HOSTS"}
                    )

        return edges
