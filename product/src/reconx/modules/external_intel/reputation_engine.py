from reconx.modules.asm_core.schema import UnifiedAsset
from reconx.modules.external_intel.schema import ReputationProfileModel

class ReputationEngine:
    """
    Computes trust scores (0-100) based on infrastructure and exposure context.
    """
    def __init__(self):
        pass

    def evaluate_reputation(self, asset: UnifiedAsset) -> ReputationProfileModel:
        # Conceptual scoring
        score = 50
        reputation = "neutral"
        factors = {}
        
        if asset.asset_type == "endpoint":
            if "admin" in asset.value.lower():
                score -= 30
                reputation = "suspicious"
                factors["admin_interface"] = "negative"
                
        elif asset.asset_type == "ip":
            # Dummy external signal mapping
            if asset.value.startswith("10.") or asset.value.startswith("192.168."):
                score += 40
                reputation = "trusted"
                factors["internal_space"] = "positive"
                
        return ReputationProfileModel(
            reputation=reputation,
            reputation_score=max(0, min(100, score)),
            factors=factors
        )
