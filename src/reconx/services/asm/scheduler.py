"""ASM scheduler for continuous attack surface monitoring."""

import threading
from typing import Callable, Dict, Optional


class AsmScheduler:
    """Simple scheduler for periodic ASM scan jobs."""

    def __init__(self):
        self._jobs: Dict[str, threading.Timer] = {}
        self._running = False

    def schedule(
        self, job_id: str, func: Callable, interval_seconds: int = 3600
    ) -> None:
        """Schedule a recurring job."""
        def _run():
            func()
            if self._running:
                self.schedule(job_id, func, interval_seconds)

        timer = threading.Timer(interval_seconds, _run)
        timer.daemon = True
        self._jobs[job_id] = timer
        self._running = True
        timer.start()

    def cancel(self, job_id: str) -> None:
        """Cancel a scheduled job."""
        timer = self._jobs.pop(job_id, None)
        if timer:
            timer.cancel()

    def cancel_all(self) -> None:
        """Cancel all scheduled jobs."""
        self._running = False
        for timer in self._jobs.values():
            timer.cancel()
        self._jobs.clear()


# Singleton instance
asm_scheduler = AsmScheduler()
