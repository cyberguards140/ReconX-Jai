import json
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

COMPLIANCE_MAPPING = {
    "SOC2": {
        "CC6.1": {
            "description": "Logical access security software, infrastructure, and architectures have been implemented.",
            "implemented_by": "reconx.security.zero_trust.evaluator",
            "status": "implemented"
        },
        "CC6.6": {
            "description": "Logical access security measures have been implemented to protect against threats from outside and inside the entity.",
            "implemented_by": "reconx.security.monitoring.threat_detector",
            "status": "implemented"
        },
        "CC6.7": {
            "description": "The entity restricts the transmission, movement, and removal of information.",
            "implemented_by": "reconx.security.encryption.cipher",
            "status": "implemented"
        }
    },
    "ISO27001": {
        "A.9.2.1": {
            "description": "User registration and de-registration",
            "implemented_by": "reconx.auth",
            "status": "implemented"
        },
        "A.10.1.1": {
            "description": "Policy on the use of cryptographic controls",
            "implemented_by": "reconx.security.encryption.cipher",
            "status": "implemented"
        },
        "A.12.4.1": {
            "description": "Event logging",
            "implemented_by": "reconx.security.audit.logger",
            "status": "implemented"
        }
    }
}

class ComplianceMapper:
    """
    Exposes a mapping of active security controls in ReconX to standard compliance frameworks.
    Useful for generating evidence for audits.
    """
    @classmethod
    def get_framework_status(cls, framework: str) -> Dict[str, Any]:
        """Returns the control mapping for a specific framework (e.g., SOC2)."""
        framework = framework.upper()
        if framework not in COMPLIANCE_MAPPING:
            raise ValueError(f"Framework {framework} not supported.")
        return COMPLIANCE_MAPPING[framework]

    @classmethod
    def get_all_mappings(cls) -> Dict[str, Any]:
        return COMPLIANCE_MAPPING
