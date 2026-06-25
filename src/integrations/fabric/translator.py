import logging
from typing import Any

logger = logging.getLogger(__name__)


class SecurityDataFabricTranslator:
    """
    Phase 71: Security Data Fabric.
    Universal translation layer that normalizes internal ReconX findings
    into the Open Cybersecurity Schema Framework (OCSF) for SIEM ingestion.
    """

    def __init__(self):
        pass

    def translate_to_ocsf(self, finding: dict[str, Any]) -> dict[str, Any]:
        """
        Translates a proprietary ReconX finding into an OCSF Vulnerability Finding (Class 2002).
        """
        logger.debug(f"[Data Fabric] Translating finding {finding.get('id')} to OCSF...")

        # OCSF Mapping
        ocsf_payload = {
            "class_uid": 2002,
            "class_name": "Vulnerability Finding",
            "metadata": {
                "product": {"name": "ReconX", "vendor_name": "ReconX Enterprise"},
                "version": "1.0.0-rc",
            },
            "vulnerabilities": [
                {
                    "cve": {"uid": finding.get("cve_id", "UNKNOWN")},
                    "severity": finding.get("severity", "Medium").capitalize(),
                }
            ],
            "device": {"ip": finding.get("target_ip"), "hostname": finding.get("target_domain")},
        }

        return ocsf_payload


fabric_translator = SecurityDataFabricTranslator()
