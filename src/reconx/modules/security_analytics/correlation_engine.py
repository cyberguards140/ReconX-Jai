from typing import Any

from reconx.modules.security_analytics.behavior_engine import BehaviorEngine
from reconx.modules.security_analytics.schema import NormalizedEventModel


class CorrelationEngine:
    """
    Correlates multiple intelligence layers (Asset + Threat + Cloud + Behavior).
    """

    def __init__(self, behavior_engine: BehaviorEngine):
        self.behavior_engine = behavior_engine

    def correlate_event(
        self, event: NormalizedEventModel, threat_context: dict[str, Any] = None
    ) -> int:
        """
        Calculates a correlated risk score.
        """
        score = 0
        profile = self.behavior_engine.get_profile(event.asset_id)

        score += profile.anomaly_score

        if threat_context and threat_context.get("risk_score", 0) > 50:
            score += 50

        if event.severity == "high":
            score += 30

        return min(100, score)
