import asyncio
from typing import Any

from reconx.schemas.normalization import NormalizedRecord


class ResultAggregator:
    def __init__(self):
        self.assets: dict[str, dict[str, Any]] = {}
        self.findings: list[dict[str, Any]] = []
        self.logs: list[str] = []
        self.records: list[NormalizedRecord] = []
        self._lock = asyncio.Lock()

    async def add_result(self, task_id: str, result: Any):  # result is a PluginResult
        async with self._lock:
            if hasattr(result, "records") and result.records:
                self.records.extend(result.records)

            for asset in getattr(result, "assets", []):
                key = f"{asset.get('type')}:{asset.get('value')}"
                if key not in self.assets:
                    self.assets[key] = asset

            for finding in getattr(result, "findings", []):
                finding["source_task"] = task_id
                self.findings.append(finding)

            for error in getattr(result, "errors", []):
                self.logs.append(f"[{task_id}] ERROR: {error}")

    def get_summary(self) -> dict[str, Any]:
        return {
            "total_assets": len(self.assets),
            "total_findings": len(self.findings),
            "total_records": len(self.records),
            "unique_assets": list(self.assets.values()),
        }
