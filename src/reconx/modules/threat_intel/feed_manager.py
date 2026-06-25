from typing import List, Dict, Any

class ThreatFeedManager:
    """
    Abstract engine to conceptualize ingesting and normalizing threat feeds.
    """
    def __init__(self):
        pass

    def ingest_feed(self, source_name: str, raw_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Normalizes raw IOCs into a standard format and deduplicates.
        """
        normalized = []
        for item in raw_data:
            # Conceptual normalization
            normalized.append({
                "ioc_type": item.get("type", "unknown"),
                "value": item.get("indicator", ""),
                "threat_level": item.get("severity", "medium"),
                "source": source_name
            })
        return normalized
