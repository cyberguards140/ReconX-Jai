from reconx.modules.analytics.prioritization import AssetPrioritization


class PrioritizationEngineService:
    @staticmethod
    def prioritize(assets: list[dict]) -> list[dict]:
        return AssetPrioritization.rank_assets(assets)
