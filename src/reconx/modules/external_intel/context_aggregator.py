from typing import Any

from reconx.modules.asm_core.schema import UnifiedAsset
from reconx.modules.external_intel.schema import ExternalIntelModel


class ContextAggregator:
    """
    Fuses internal asset data and external signals into a unified profile.
    """

    def __init__(self):
        pass

    def aggregate(self, asset: UnifiedAsset, external_intel: ExternalIntelModel) -> dict[str, Any]:
        """
        Calculates a final intelligence score.
        """
        internal_risk = 50.0 - asset.confidence  # basic inversion heuristic
        exposure_risk = 30.0 if external_intel.exposure.internet_visibility else 10.0
        reputation_risk = 100.0 - external_intel.reputation.reputation_score
        threat_score = len(external_intel.threat_indicators) * 15.0

        final_score = internal_risk + exposure_risk + reputation_risk + threat_score

        return {
            "asset_id": asset.asset_id,
            "internal_data_summary": asset.model_dump(),
            "external_intel_summary": external_intel.model_dump(),
            "final_intelligence_score": min(100.0, final_score),
        }
