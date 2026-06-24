class AssetPrioritization:
    @staticmethod
    def rank_assets(assets: list[dict]) -> list[dict]:
        # Sort by risk_score desc
        sorted_assets = sorted(assets, key=lambda x: x.get("risk_score", 0.0), reverse=True)
        for i, asset in enumerate(sorted_assets):
            asset["priority_rank"] = i + 1
        return sorted_assets
