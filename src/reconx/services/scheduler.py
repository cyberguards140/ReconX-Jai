from reconx.modules.automation.scheduler import AutomationSchedulerCore


class SchedulerService:
    @staticmethod
    def check_schedule(interval: str, last_run: str) -> bool:
        return AutomationSchedulerCore.is_due(interval, last_run)
