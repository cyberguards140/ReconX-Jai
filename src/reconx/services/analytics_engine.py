class AnalyticsEngine:
    @staticmethod
    def build_asset_profile(asset_id: str, ip: str, services: int, findings: int, risk_score: float) -> dict:
        return {
            "asset_id": asset_id,
            "ip": ip,
            "service_count": services,
            "finding_count": findings,
            "risk_score": risk_score
        }
