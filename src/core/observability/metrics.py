import time
import logging

logger = logging.getLogger(__name__)

class MetricsRegistry:
    """
    Mock Prometheus/OpenTelemetry metrics registry for MVP.
    Tracks RED (Rate, Errors, Duration) metrics.
    """
    def __init__(self):
        self.scans_completed = 0
        self.scans_failed = 0
        self.active_workers = 0
        self.total_assets_discovered = 0
        self._start_time = time.time()

    def increment_scans(self, success: bool = True):
        if success:
            self.scans_completed += 1
        else:
            self.scans_failed += 1

    def update_workers(self, count: int):
        self.active_workers = count
        
    def add_assets(self, count: int):
        self.total_assets_discovered += count

    def generate_prometheus_payload(self) -> str:
        """
        Generates a standard Prometheus /metrics payload.
        """
        uptime = time.time() - self._start_time
        return f"""# HELP reconx_scans_completed_total Total number of successful scans
# TYPE reconx_scans_completed_total counter
reconx_scans_completed_total {self.scans_completed}

# HELP reconx_scans_failed_total Total number of failed scans
# TYPE reconx_scans_failed_total counter
reconx_scans_failed_total {self.scans_failed}

# HELP reconx_active_workers Current number of active regional workers
# TYPE reconx_active_workers gauge
reconx_active_workers {self.active_workers}

# HELP reconx_assets_discovered_total Total assets discovered
# TYPE reconx_assets_discovered_total counter
reconx_assets_discovered_total {self.total_assets_discovered}

# HELP reconx_uptime_seconds Process uptime
# TYPE reconx_uptime_seconds counter
reconx_uptime_seconds {uptime:.2f}
"""

metrics_registry = MetricsRegistry()
