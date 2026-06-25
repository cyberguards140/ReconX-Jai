import logging
import os
from typing import Any

import aiohttp

logger = logging.getLogger(__name__)


class AlertNotifier:
    """
    Subscribes to Critical/High risk findings and dispatches Webhooks to multiple channels.
    """

    def __init__(self):
        # MVP: Pull webhook URLs from environment variables
        self.slack_webhook = os.environ.get("RECONX_SLACK_WEBHOOK")
        self.discord_webhook = os.environ.get("RECONX_DISCORD_WEBHOOK")
        self.teams_webhook = os.environ.get("RECONX_TEAMS_WEBHOOK")
        self.generic_webhook = os.environ.get("RECONX_GENERIC_WEBHOOK")

    async def handle_result(self, result_payload: dict[str, Any]):
        """
        Callback bound to the global Message Broker for the 'store_results' queue.
        """
        stage = result_payload.get("stage")
        if stage != "vulnerability_scan" and stage != "enrichment":
            return  # Only alert on verified vulnerabilities or enrichment correlated risks

        task = result_payload.get("original_task", {})
        findings = task.get("findings", [])  # Assuming the worker injected findings here

        for finding in findings:
            severity = (
                finding.get("severity", "").lower()
                if isinstance(finding, dict)
                else getattr(finding, "severity", "").lower()
            )
            if severity in ["high", "critical"]:
                await self.dispatch_alert(finding)

    async def dispatch_alert(self, finding: Any):
        title = (
            finding.get("title")
            if isinstance(finding, dict)
            else getattr(finding, "title", "Unknown")
        )
        target = (
            finding.get("asset_target")
            if isinstance(finding, dict)
            else getattr(finding, "asset_target", "Unknown")
        )
        severity = (
            finding.get("severity")
            if isinstance(finding, dict)
            else getattr(finding, "severity", "Unknown")
        )

        msg = f"🚨 **{severity.upper()} Alert**: {title} discovered on `{target}`!"
        logger.warning(f"Dispatching Alert: {msg}")

        async with aiohttp.ClientSession() as session:
            if self.slack_webhook:
                await session.post(self.slack_webhook, json={"text": msg})
            if self.discord_webhook:
                await session.post(self.discord_webhook, json={"content": msg})
            if self.teams_webhook:
                await session.post(self.teams_webhook, json={"text": msg})
            if self.generic_webhook:
                await session.post(
                    self.generic_webhook,
                    json={"message": msg, "severity": severity, "target": target},
                )


alert_notifier = AlertNotifier()
