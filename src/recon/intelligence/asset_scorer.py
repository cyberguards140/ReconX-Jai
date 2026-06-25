import logging
from typing import Any

logger = logging.getLogger(__name__)


class AssetIntelligenceEngine:
    """
    Phase 64: Asset Intelligence Engine.
    Calculates multi-dimensional intelligence scores for an asset.
    """

    def __init__(self):
        pass

    def calculate_scores(self, asset: dict[str, Any]) -> dict[str, int]:
        """
        Calculates Risk, Business, Exposure, and Confidence scores based on asset metadata.
        """
        scores = {
            "risk_score": 0,
            "business_score": 0,
            "exposure_score": 0,
            "confidence_score": 100,
        }

        target_name = asset.get("target", "").lower()

        # Infer Business Score from keywords
        if any(keyword in target_name for keyword in ["prod", "billing", "api", "admin", "secure"]):
            scores["business_score"] += 80
        elif any(keyword in target_name for keyword in ["dev", "test", "staging"]):
            scores["business_score"] += 30

        # Calculate Exposure Score
        if asset.get("is_public", False):
            scores["exposure_score"] += 50
            if asset.get("open_ports", []):
                scores["exposure_score"] += len(asset["open_ports"]) * 5

        # Calculate Base Risk Score
        scores["risk_score"] = int(
            (scores["business_score"] * 0.4) + (scores["exposure_score"] * 0.6)
        )

        logger.info(f"[Asset Intel Engine] Calculated Scores for {target_name}: {scores}")
        return scores


asset_scorer = AssetIntelligenceEngine()
