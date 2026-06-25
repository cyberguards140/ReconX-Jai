import logging
import re
from typing import Dict, Any

logger = logging.getLogger(__name__)

class ExposureEngine:
    """
    Analyzes asset metadata (HTML title, headers, Shodan tags) to detect
    critical exposures like Admin Panels, VPNs, and internal infrastructure.
    """
    def __init__(self):
        self.exposure_signatures = {
            "Admin Panel": [r"admin login", r"wp-admin", r"dashboard", r"control panel"],
            "VPN Portal": [r"pulse secure", r"cisco anyconnect", r"globalprotect", r"fortinet"],
            "CI/CD": [r"jenkins", r"gitlab", r"travis ci", r"teamcity"],
            "Observability": [r"grafana", r"kibana", r"prometheus", r"datadog"]
        }

    def evaluate_exposure(self, asset: Dict[str, Any]) -> Dict[str, Any]:
        """
        Scans an asset for exposure signatures and tags it accordingly.
        """
        metadata_str = str(asset.get("metadata", "")).lower()
        title_str = str(asset.get("title", "")).lower()
        
        combined_text = f"{metadata_str} {title_str}"
        
        exposures_found = []
        
        for category, patterns in self.exposure_signatures.items():
            for pattern in patterns:
                if re.search(pattern, combined_text):
                    exposures_found.append(category)
                    break # Move to next category to avoid duplicates

        if exposures_found:
            asset["exposure_tags"] = exposures_found
            asset["is_critical_exposure"] = True
            logger.warning(f"Critical Exposures detected on {asset.get('target')}: {exposures_found}")
        else:
            asset["exposure_tags"] = []
            asset["is_critical_exposure"] = False
            
        return asset

exposure_engine = ExposureEngine()
