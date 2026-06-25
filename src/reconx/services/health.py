class HealthService:
    @staticmethod
    def check_health() -> dict:
        return {"status": "healthy", "components": {"database": "up", "workers": "up", "api": "up"}}

    @staticmethod
    def check_ready() -> dict:
        return {"ready": True}
