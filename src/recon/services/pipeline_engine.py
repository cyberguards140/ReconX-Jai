import logging
from typing import Any

from core.messaging.broker import broker

logger = logging.getLogger(__name__)


class PipelineOrchestrator:
    """
    Central orchestrator for the distributed pipeline.
    It no longer runs local workers. It publishes tasks to the global broker
    and advances the workflow when workers report completion.
    """

    def __init__(self):
        # Register a callback to handle results coming back from distributed workers
        broker.subscribe("store_results", self._handle_worker_result)

        # Register Alert Notifier for Critical findings
        from core.events.notifier import alert_notifier

        broker.subscribe("store_results", alert_notifier.handle_result)

    async def _handle_worker_result(self, result_payload: dict[str, Any]):
        """Callback fired when a remote worker finishes a task."""
        task = result_payload.get("original_task", {})
        target = task.get("target")
        stage = result_payload.get("stage")

        logger.info(
            f"[Orchestrator] Worker {result_payload.get('worker_id')} finished {stage} for {target}"
        )

        # Advance the DAG
        if stage == "subfinder":
            await self.enqueue("amass", {"target": target})
        elif stage == "amass":
            await self.enqueue("assetfinder", {"target": target})
        elif stage == "assetfinder":
            await self.enqueue("dnsx", {"target": target})
        elif stage == "dnsx":
            await self.enqueue("naabu", {"target": target})
        elif stage == "naabu":
            await self.enqueue("nmap", {"target": target})
        elif stage == "nmap":
            await self.enqueue("httpx", {"target": target})
        elif stage == "httpx":
            await self.enqueue("gowitness", {"target": target, "url": "http://" + target})
        elif stage == "gowitness":
            await self.enqueue("katana", {"target": target})
        elif stage == "katana":
            await self.enqueue("secrets_scan", {"target": target})
        elif stage == "secrets_scan":
            await self.enqueue("vulnerability_scan", {"target": target})
        elif stage == "vulnerability_scan":
            await self.enqueue("enrichment", {"target": target})
        elif stage == "enrichment":
            logger.info(f"Pipeline complete for {target}. Committing to Correlation Engine.")
            # Fire and forget enrichment (in a real system this would happen asynchronously within the stage worker)
            import asyncio

            from recon.intelligence.exposure import exposure_engine
            from recon.intelligence.threat_intel import threat_intel_engine
            from recon.processing.correlation_engine import CorrelationEngine

            async def run_enrichment():
                enriched_asset = await threat_intel_engine.enrich_asset(task)
                final_asset = exposure_engine.evaluate_exposure(enriched_asset)
                CorrelationEngine.process_result(final_asset)

            asyncio.create_task(run_enrichment())

    async def enqueue(self, stage: str, task: dict[str, Any]):
        """Publish a task to the distributed broker."""
        logger.info(f"[Orchestrator] Enqueueing {task.get('target')} to {stage} queue")
        await broker.publish(stage, task)

    def start(self):
        import asyncio

        logger.info("Pipeline Orchestrator connected to Distributed Broker")
        # Start the consumer loop for store_results so the orchestrator can listen
        asyncio.create_task(broker.start_consumer("store_results"))

    async def stop(self):
        logger.info("Pipeline Orchestrator disconnected")


pipeline_engine = PipelineOrchestrator()
