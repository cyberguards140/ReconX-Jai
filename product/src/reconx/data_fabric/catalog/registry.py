import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

class MetadataCatalog:
    """
    Enterprise Schema Registry and Data Discovery platform.
    """
    def __init__(self):
        self._registry = {
            "assets": {
                "description": "Enterprise Asset Inventory (Cloud & On-Prem)",
                "schema": {"ip": "string", "hostname": "string", "vulnerabilities": "list"},
                "classification": "Internal",
                "owner": "ASM Team"
            },
            "threat_intelligence": {
                "description": "Global Threat Feeds and IOCs",
                "schema": {"indicator": "string", "type": "string", "confidence": "float"},
                "classification": "Public",
                "owner": "CTI Team"
            },
            "incidents": {
                "description": "High-confidence security incidents and alerts",
                "schema": {"incident_id": "string", "severity": "string", "status": "string"},
                "classification": "Confidential",
                "owner": "SOC Team"
            }
        }

    def get_catalog(self) -> Dict[str, Any]:
        """Returns the available datasets in the Lakehouse."""
        return self._registry
        
    def get_schema(self, dataset: str) -> Dict[str, Any]:
        return self._registry.get(dataset, {})

metadata_catalog = MetadataCatalog()
