import logging
from typing import Any

logger = logging.getLogger(__name__)


class ExposureMonitoringNetwork:
    """
    Phase 69: Exposure Monitoring Network.
    A reactive event bus that fires real-time alerts when asset states change.
    """

    def __init__(self):
        pass

    async def on_asset_discovered(self, asset: dict[str, Any]):
        """
        Triggered when the Timeline Engine logs a 'created' event.
        """
        target = asset.get("target")
        logger.warning(f"[Exposure Monitor] REAL-TIME ALERT: New Asset Discovered -> {target}")
        # In production: Push to Slack/Teams webhook immediately

    async def on_dns_drift(self, domain: str, old_ip: str, new_ip: str):
        """
        Triggered when historical domain IP resolution changes unexpectedly.
        """
        logger.critical(
            f"[Exposure Monitor] REAL-TIME ALERT: DNS Drift detected on {domain} ({old_ip} -> {new_ip})! Potential Hijack!"
        )


exposure_monitor = ExposureMonitoringNetwork()
