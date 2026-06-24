class MonitoringCore:
    @staticmethod
    def diff_assets(old_assets: list[str], new_assets: list[str]) -> dict:
        added = list(set(new_assets) - set(old_assets))
        removed = list(set(old_assets) - set(new_assets))
        return {"added": added, "removed": removed}
