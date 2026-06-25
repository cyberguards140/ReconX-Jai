from reconx.modules.automation.monitoring import MonitoringCore


class MonitoringEngineService:
    @staticmethod
    def analyze_changes(old_assets: list[str], new_assets: list[str]) -> list[dict]:
        diff = MonitoringCore.diff_assets(old_assets, new_assets)
        events = []
        for a in diff["added"]:
            events.append({"type": "Added", "asset": a})
        for r in diff["removed"]:
            events.append({"type": "Removed", "asset": r})
        return events
