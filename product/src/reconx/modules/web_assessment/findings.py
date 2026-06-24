from reconx.database.models import SeverityEnum

class SeverityMapper:
    @staticmethod
    def map_severity(tool: str, raw_severity: str) -> SeverityEnum:
        raw = raw_severity.lower()
        if "crit" in raw or "high" in raw:
            return SeverityEnum.high
        elif "med" in raw or "warn" in raw:
            return SeverityEnum.medium
        elif "low" in raw:
            return SeverityEnum.low
        return SeverityEnum.info
