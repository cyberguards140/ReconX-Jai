from reconx.modules.analytics.correlation_engine import AnalyticsCorrelationEngine

class GlobalCorrelationEngine:
    @staticmethod
    def correlate(findings: list[dict]) -> list[dict]:
        return AnalyticsCorrelationEngine.merge_finding_duplicates(findings)
