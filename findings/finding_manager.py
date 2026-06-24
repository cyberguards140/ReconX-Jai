class FindingManager:
    def normalize_severity(self, raw_severity):
        mapping = {
            "critical": "Critical",
            "high": "High",
            "medium": "Medium",
            "low": "Low",
            "info": "Info",
            "informational": "Info"
        }
        return mapping.get(str(raw_severity).lower(), "Info")
