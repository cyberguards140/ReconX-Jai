import asyncio
import logging
from datetime import datetime, timezone
from croniter import croniter
from sqlalchemy import select
from reconx.database.models import ReportSchedule
from reconx.reporting.engine.report_engine import ReportEngine

logger = logging.getLogger(__name__)

class ReportScheduler:
    def __init__(self, session_maker, report_engine: ReportEngine):
        self.session_maker = session_maker
        self.report_engine = report_engine
        self._running = False
        self._task = None

    async def start(self):
        """Start the scheduler background loop."""
        if self._running:
            return
        self._running = True
        self._task = asyncio.create_task(self._run_loop())
        logger.info("ReportScheduler started.")

    async def stop(self):
        """Stop the scheduler background loop."""
        self._running = False
        if self._task:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass
        logger.info("ReportScheduler stopped.")

    async def _run_loop(self):
        while self._running:
            try:
                await self._check_and_run_schedules()
            except Exception as e:
                logger.error(f"Error in scheduler loop: {e}")
            
            # Sleep before checking again
            await asyncio.sleep(60)

    async def _check_and_run_schedules(self):
        now = datetime.now(timezone.utc)
        
        async with self.session_maker() as session:
            stmt = select(ReportSchedule).where(ReportSchedule.status == "active")
            result = await session.execute(stmt)
            schedules = result.scalars().all()

            for schedule in schedules:
                try:
                    if not schedule.next_run:
                        # Initialize next_run
                        cron = croniter(schedule.cron_expression, now)
                        schedule.next_run = cron.get_next(datetime).replace(tzinfo=timezone.utc)
                        session.add(schedule)
                        continue

                    # If next_run is strictly naive, make it aware (for safety)
                    if schedule.next_run.tzinfo is None:
                        schedule.next_run = schedule.next_run.replace(tzinfo=timezone.utc)

                    if now >= schedule.next_run:
                        logger.info(f"Running scheduled report {schedule.id} ({schedule.report_type})")
                        
                        # Trigger report generation
                        # We pass a default scope, or parse it from schedule config if we had it
                        if schedule.report_type == "Executive":
                            await self.report_engine.generate_executive_report(
                                session=session,
                                target_scope=f"Tenant-{schedule.tenant_id}",
                                title=f"Scheduled Executive Report - {now.strftime('%Y-%m-%d')}",
                                export_format="pdf"
                            )
                        elif schedule.report_type == "Technical":
                            await self.report_engine.generate_technical_report(
                                session=session,
                                target_scope=f"Tenant-{schedule.tenant_id}",
                                title=f"Scheduled Technical Report - {now.strftime('%Y-%m-%d')}",
                                export_format="json"
                            )

                        # Update timestamps
                        schedule.last_run = now
                        cron = croniter(schedule.cron_expression, now)
                        schedule.next_run = cron.get_next(datetime).replace(tzinfo=timezone.utc)
                        session.add(schedule)

                except Exception as e:
                    logger.error(f"Failed to process schedule {schedule.id}: {e}")

            await session.commit()
