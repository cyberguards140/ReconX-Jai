from reconx.modules.security_analytics.schema import BehaviorBaselineModel, NormalizedEventModel


class BehaviorEngine:
    """
    Builds behavioral baselines and tracks anomalies.
    """

    def __init__(self):
        self.profiles = {}

    def update_baseline(self, event: NormalizedEventModel):
        if event.asset_id not in self.profiles:
            self.profiles[event.asset_id] = BehaviorBaselineModel(entity=event.asset_id)

        # Conceptual anomaly increase
        if event.severity in ["high", "critical"]:
            self.profiles[event.asset_id].anomaly_score += 10

    def get_profile(self, entity_id: str) -> BehaviorBaselineModel:
        return self.profiles.get(entity_id, BehaviorBaselineModel(entity=entity_id))
