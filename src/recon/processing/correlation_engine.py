import logging
from typing import Any

from data.database.models import Asset
from data.database.session import SessionLocal

logger = logging.getLogger(__name__)


class CorrelationEngine:
    @staticmethod
    def process_result(task: dict[str, Any]):
        """
        Process results from the pipeline, deduplicate, correlate intelligence, and store in DB.
        """
        target = task.get("target")
        source = task.get("source", "Pipeline")
        confidence = task.get("confidence", 0.5)

        # Intelligence data points
        threat_intel = task.get("threat_intel", {})
        is_critical_exposure = task.get("is_critical_exposure", False)

        with SessionLocal() as db:
            # Deduplication logic
            existing_asset = db.query(Asset).filter(Asset.value == target).first()

            if existing_asset:
                logger.info(f"Asset {target} already exists. Correlating...")
                # Update sources array
                sources = existing_asset.sources or []
                if source not in sources:
                    sources.append(source)
                    existing_asset.sources = sources

                # Max confidence
                if confidence > existing_asset.confidence:
                    existing_asset.confidence = confidence

                asset = existing_asset
            else:
                logger.info(f"New asset discovered: {target}")
                asset = Asset(
                    project_id="default",
                    asset_type="domain",
                    value=target,
                    sources=[source],
                    confidence=confidence,
                    lifecycle_status="active",
                    tags=[],
                )
                db.add(asset)

            db.commit()

            # --- Advanced Intelligence Correlation ---
            risk_score = 0

            # 1. Shodan Ports Correlation
            shodan_ports = threat_intel.get("shodan", {}).get("ports", [])
            if 22 in shodan_ports or 3389 in shodan_ports:
                risk_score += 30

            # 2. VirusTotal Malicious Correlation
            vt_malicious = threat_intel.get("virustotal", {}).get("malicious", 0)
            if vt_malicious > 0:
                risk_score += 50

            # 3. Exposure Correlation
            if is_critical_exposure:
                risk_score += 40

            # Trigger High Priority Alert if Risk exceeds threshold
            if risk_score >= 70:
                logger.critical(
                    f"HIGH PRIORITY RISK ALERT: Asset {target} has reached critical mass ({risk_score}/100) due to complex correlation chains!"
                )
                # In a real app, this would push directly to the Webhook/Alerting Engine or create a critical Vulnerability Finding
                import asyncio

                from core.events.notifier import alert_notifier

                # Fire and forget alert
                asyncio.create_task(
                    alert_notifier.dispatch_alert(
                        {
                            "title": "Correlated Intelligence High-Risk Asset",
                            "asset_target": target,
                            "severity": "critical",
                        }
                    )
                )
