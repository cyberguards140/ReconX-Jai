import uuid
from typing import Dict, Any
from reconx.modules.infra_intel.schema import ASNNode

class ASNMapper:
    """
    Normalizes ASN metadata and extracts associated netblocks.
    """
    def __init__(self):
        pass

    def map_asn(self, raw_data: Dict[str, Any]) -> ASNNode:
        """
        Maps raw ASN data to an ASNNode.
        """
        value = raw_data.get("asn", "")
        if not value.startswith("AS"):
            value = f"AS{value}"
            
        return ASNNode(
            id=str(uuid.uuid4()),
            value=value,
            name=raw_data.get("name"),
            country=raw_data.get("country"),
            netblocks=raw_data.get("netblocks", []),
            metadata=raw_data.get("metadata", {})
        )
