class RecommendationGenerator:
    @staticmethod
    def generate_recommendations(findings: list[dict]) -> list[dict]:
        recs = []
        tls_issues = [f for f in findings if "TLS" in f.get("title", "")]
        if len(tls_issues) > 0:
            recs.append({
                "recommendation_id": "rec-tls",
                "title": "Upgrade TLS Configurations",
                "description": "Multiple assets are running outdated or weak TLS configurations.",
                "impact": "High Impact",
                "affected_assets": len(set([f.get("asset_id") for f in tls_issues]))
            })
        return recs
