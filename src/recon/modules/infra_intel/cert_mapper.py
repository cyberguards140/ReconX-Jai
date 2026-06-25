import uuid
from typing import Any

from recon.modules.infra_intel.schema import CertificateNode


class CertMapper:
    """
    Normalizes Certificate data.
    """

    def __init__(self):
        pass

    def map_certificate(self, raw_data: dict[str, Any]) -> CertificateNode:
        """
        Maps raw certificate data to a CertificateNode.
        """
        value = raw_data.get("cert_id", str(uuid.uuid4()))

        return CertificateNode(
            id=str(uuid.uuid4()),
            value=value,
            issuer=raw_data.get("issuer"),
            subject=raw_data.get("subject"),
            domains=raw_data.get("domains", []),
            metadata=raw_data.get("metadata", {}),
        )
