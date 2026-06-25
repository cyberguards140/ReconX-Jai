from reconx.modules.security_analytics.schema import DetectionRuleModel, NormalizedEventModel


class DetectionEngine:
    """
    Evaluates normalized events against detection logic and thresholds.
    """

    def __init__(self):
        self.rules: list[DetectionRuleModel] = []

    def load_rule(self, rule: DetectionRuleModel):
        self.rules.append(rule)

    def evaluate_event(self, event: NormalizedEventModel) -> bool:
        """
        Abstract evaluation. Returns True if a rule is triggered.
        """
        for rule in self.rules:
            # Conceptual condition matching
            if event.event_type in str(rule.conditions):
                return True
        return False
