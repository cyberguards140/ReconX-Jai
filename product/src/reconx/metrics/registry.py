from typing import Dict, Any
from prometheus_client import Counter, Histogram

class MetricsRegistry:
    def __init__(self):
        self._counters: Dict[str, Counter] = {}
        self._timers: Dict[str, Histogram] = {}

    def increment(self, metric: str, amount: int = 1):
        if metric not in self._counters:
            self._counters[metric] = Counter(metric, f"Count of {metric}")
        self._counters[metric].inc(amount)

    def record_time(self, metric: str, duration: float):
        if metric not in self._timers:
            self._timers[metric] = Histogram(metric, f"Duration of {metric}")
        self._timers[metric].observe(duration)

    def get_metrics(self) -> Dict[str, Any]:
        return {} # Let /metrics route handle it with generate_latest()

metrics_registry = MetricsRegistry()
