class AutomationSchedulerCore:
    @staticmethod
    def is_due(interval: str, last_run: str) -> bool:
        # Simplified cron logic for testing
        if not last_run:
            return True
        # Mock logic
        return interval == "Hourly"
