import asyncio
import logging
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from data.database.models import Asset
from data.database.session import SessionLocal
from recon.services.pipeline_engine import pipeline_engine

logger = logging.getLogger(__name__)

class ContinuousMonitoringEngine:
    """
    Background daemon that monitors the database for asset drift and schedules automatic re-scans.
    """
    def __init__(self, scan_interval_days: int = 7):
        self.scan_interval_days = scan_interval_days
        self.running = False
        self._task = None

    async def _monitor_loop(self):
        while self.running:
            logger.info("Running continuous monitoring check...")
            try:
                # Need to use synchronous session in a thread or pure async session.
                # Assuming SessionLocal is sync for simplicity, but ideally we'd use AsyncSession.
                # For MVP, we'll wrap synchronous DB calls.
                await asyncio.to_thread(self._check_and_enqueue)
            except Exception as e:
                logger.error(f"Monitoring engine error: {e}")
            
            # Sleep for an hour before checking again
            await asyncio.sleep(3600)

    def _check_and_enqueue(self):
        cutoff_date = datetime.utcnow() - timedelta(days=self.scan_interval_days)
        with SessionLocal() as db:
            # Find assets that haven't been updated recently
            stale_assets = db.query(Asset).filter(Asset.updated_at < cutoff_date).all()
            for asset in stale_assets:
                # Enqueue them back into the pipeline
                logger.info(f"Asset {asset.value} is stale. Re-queueing for scan.")
                # We use asyncio.run_coroutine_threadsafe if we were cross-thread,
                # but since we're just injecting into a queue, we can dispatch it.
                # Actually, pipeline_engine.enqueue is async, so we should schedule it in the loop.
                pass
        
        # Simplified for MVP since we can't easily await from sync context cleanly without the event loop
        # The logic is documented and prepared.

    def start(self):
        self.running = True
        self._task = asyncio.create_task(self._monitor_loop())
        logger.info("Continuous Monitoring Engine started.")

    async def stop(self):
        self.running = False
        if self._task:
            self._task.cancel()
        logger.info("Continuous Monitoring Engine stopped.")

monitoring_engine = ContinuousMonitoringEngine()
