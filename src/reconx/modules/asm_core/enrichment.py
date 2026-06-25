from typing import List, Dict, Any
from reconx.modules.asm_core.schema import UnifiedAsset

class EnrichmentEngine:
    """
    Enrichment layer for ASM Core. Adds intelligence, service classification,
    and exposure hints based on metadata.
    """
    def __init__(self):
        pass

    def enrich_asset(self, asset: UnifiedAsset) -> Dict[str, Any]:
        """
        Derive enrichments based on asset metadata.
        Returns a dictionary of enrichment data (e.g., tech_guess, exposure).
        """
        enrichment_data = {
            "tech_guess": [],
            "exposure": "internal",
            "service_type": "unknown"
        }
        
        # Simple structural heuristics
        if asset.asset_type in ("domain", "subdomain", "url"):
            enrichment_data["exposure"] = "internet-facing"
            
        tech_list = asset.metadata.get("tech", [])
        if "nginx" in tech_list or "apache" in tech_list:
            enrichment_data["service_type"] = "web server"
            
        if "login" in asset.value.lower():
            enrichment_data["tech_guess"].append("login portal")
            
        return enrichment_data

    def process(self, asset: UnifiedAsset) -> UnifiedAsset:
        """
        Process the asset and append enrichments to its metadata.
        """
        enrichments = self.enrich_asset(asset)
        asset.metadata["enrichments"] = enrichments
        return asset
