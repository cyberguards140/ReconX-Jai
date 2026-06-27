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
        self.running = False
        
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

        import asyncio
        import uuid
        from data.database.models import Finding
        from data.database.repositories.finding import finding_repo
        from data.database.repositories.scan import scan_repo
        import datetime
        from data.database.session import async_session_factory
        
        status = result_payload.get("status", "completed")
        scan_id = task.get("scan_id", "unknown")

        if status == "failed":
            asyncio.create_task(broker.publish("ws_broadcast", {
                "type": "terminal_output", 
                "content": f"Worker FAILED {stage} for {target}",
                "tool_id": "pipeline",
                "output_type": "stderr"
            }))
            asyncio.create_task(broker.publish("ws_broadcast", {
                "type": "job_status", 
                "tool_id": stage, 
                "status": "failed"
            }))
            asyncio.create_task(broker.publish("ws_broadcast", {
                "type": "job_status", 
                "tool_id": "all", 
                "status": "failed"
            }))
            # Stop the pipeline for this scan
            try:
                async with async_session_factory() as db:
                    scan_record = await scan_repo.get(db, scan_id)
                    if scan_record:
                        await scan_repo.update(db, db_obj=scan_record, obj_in={"status": "failed", "finished_at": datetime.datetime.utcnow()})
            except Exception:
                pass
            return

        finding_id = str(uuid.uuid4())
        try:
            async with async_session_factory() as db:
                await finding_repo.create(db, obj_in={
                    "id": finding_id,
                    "scan_id": scan_id,
                    "title": f"Discovered by {stage}",
                    "severity": "info",
                    "capability": "Reconnaissance",
                    "source": stage,
                    "asset_id": "unknown"
                })
        except Exception as e:
            logger.error(f"Failed to create mock finding: {e}")

        asyncio.create_task(broker.publish("ws_broadcast", {
            "type": "terminal_output", 
            "content": f"Worker finished {stage} for {target}",
            "tool_id": "pipeline",
            "output_type": "stdout"
        }))
        asyncio.create_task(broker.publish("ws_broadcast", {
            "type": "job_status", 
            "tool_id": stage, 
            "status": "completed"
        }))

        # Advance the DAG
        next_stage = None
        if stage == "subfinder":
            next_stage = "amass"
            await self.enqueue("amass", {"target": target, "scan_id": scan_id})
        elif stage == "amass":
            next_stage = "assetfinder"
            await self.enqueue("assetfinder", {"target": target, "scan_id": scan_id})
        elif stage == "assetfinder":
            next_stage = "dnsx"
            await self.enqueue("dnsx", {"target": target, "scan_id": scan_id})
        elif stage == "dnsx":
            next_stage = "naabu"
            await self.enqueue("naabu", {"target": target, "scan_id": scan_id})
        elif stage == "naabu":
            next_stage = "nmap"
            await self.enqueue("nmap", {"target": target, "scan_id": scan_id})
        elif stage == "nmap":
            next_stage = "httpx"
            await self.enqueue("httpx", {"target": target, "scan_id": scan_id})
        elif stage == "httpx":
            next_stage = "gowitness"
            await self.enqueue("gowitness", {"target": target, "url": "http://" + target, "scan_id": scan_id})
        elif stage == "gowitness":
            next_stage = "katana"
            await self.enqueue("katana", {"target": target, "scan_id": scan_id})
        elif stage == "katana":
            next_stage = "secrets_scan"
            await self.enqueue("secrets_scan", {"target": target, "scan_id": scan_id})
        elif stage == "secrets_scan":
            next_stage = "vulnerability_scan"
            await self.enqueue("vulnerability_scan", {"target": target, "scan_id": scan_id})
        elif stage == "vulnerability_scan":
            next_stage = "enrichment"
            await self.enqueue("enrichment", {"target": target, "scan_id": scan_id})
        elif stage == "enrichment":
            logger.info(f"Pipeline complete for {target}. Committing to Correlation Engine.")
            
            # Mark scan as completed
            try:
                async with async_session_factory() as db:
                    scan_record = await scan_repo.get(db, scan_id)
                    if scan_record:
                        await scan_repo.update(db, db_obj=scan_record, obj_in={"status": "completed", "finished_at": datetime.datetime.utcnow()})
            except Exception as e:
                logger.error(f"Failed to complete scan record: {e}")
            asyncio.create_task(broker.publish("ws_broadcast", {
                "type": "terminal_output", 
                "content": f"Pipeline complete for {target}",
                "tool_id": "pipeline",
                "output_type": "stdout"
            }))
            asyncio.create_task(broker.publish("ws_broadcast", {
                "type": "job_status", 
                "tool_id": "all",
                "status": "completed"
            }))
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
        target = task.get('target', 'unknown')
        logger.info(f"[Orchestrator] Enqueueing {target} to {stage} queue")
        
        import asyncio
        asyncio.create_task(broker.publish("ws_broadcast", {
            "type": "terminal_output", 
            "content": f"Enqueued {target} for {stage}",
            "tool_id": "pipeline",
            "output_type": "stdout"
        }))
        asyncio.create_task(broker.publish("ws_broadcast", {
            "type": "job_status", 
            "tool_id": stage, 
            "status": "running"
        }))
        
        await broker.publish(stage, task)

    def start(self):
        import asyncio

        self.running = True
        logger.info("Pipeline Orchestrator connected to Distributed Broker")
        # Start the consumer loop for store_results so the orchestrator can listen
        asyncio.create_task(broker.start_consumer("store_results"))

    async def stop(self):
        self.running = False
        logger.info("Pipeline Orchestrator disconnected")


pipeline_engine = PipelineOrchestrator()
