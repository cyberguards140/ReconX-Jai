from reconx.modules.analytics.scoring import RiskScoringModel


class AnalyticsRiskEngine:
    @staticmethod
    def calculate_weighted_risk(
        critical: int, high: int, medium: int, criticality: str, exposure: str
    ) -> float:
        base_score = RiskScoringModel.compute_base_score(critical, high, medium)
        multiplier = 1.0

        if criticality == "High":
            multiplier += 0.5
        elif criticality == "Critical":
            multiplier += 1.0

        if exposure == "External":
            multiplier += 0.5

        return float(min(100.0, base_score * multiplier))
