import uuid
from typing import Any

from reconx.modules.infra_intel.schema import OrganizationNode


class OrgMapper:
    """
    Groups entities like WHOIS domain info and cert subjects to an Organization.
    """

    def __init__(self):
        pass

    def map_organization(self, raw_data: dict[str, Any]) -> OrganizationNode:
        """
        Maps raw organization data to an OrganizationNode.
        """
        value = raw_data.get("organization", "Unknown Organization")

        return OrganizationNode(
            id=str(uuid.uuid4()),
            value=value,
            domains=raw_data.get("domains", []),
            infrastructure=raw_data.get("infrastructure", []),
            metadata=raw_data.get("metadata", {}),
        )
