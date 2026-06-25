class RiskScoringModel:
    @staticmethod
    def compute_base_score(critical: int, high: int, medium: int) -> float:
        return float(min(100.0, (critical * 25.0 + high * 10.0 + medium * 5.0)))
