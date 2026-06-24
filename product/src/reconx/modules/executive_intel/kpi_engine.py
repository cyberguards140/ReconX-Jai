from reconx.modules.executive_intel.schema import KPIDashboardModel
from typing import Dict

class KPIEngine:
    """
    Aggregates operational data into executive-level key performance indicators.
    """
    def __init__(self):
        self.dashboard = KPIDashboardModel()

    def update_metrics(self, new_metrics: Dict[str, float]):
        self.dashboard.metrics.update(new_metrics)

    def get_dashboard(self) -> KPIDashboardModel:
        return self.dashboard
