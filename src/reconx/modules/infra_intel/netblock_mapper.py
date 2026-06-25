import uuid
from typing import Any

from reconx.modules.infra_intel.schema import NetblockNode


class NetblockMapper:
    """
    Abstract mapping from IP to CIDR grouping/Netblock entity.
    """

    def __init__(self):
        pass

    def map_netblock(self, raw_data: dict[str, Any]) -> NetblockNode:
        """
        Maps raw netblock data to a NetblockNode.
        """
        value = raw_data.get("netblock", "")

        return NetblockNode(
            id=str(uuid.uuid4()),
            value=value,
            owner_asn=raw_data.get("owner_asn"),
            metadata=raw_data.get("metadata", {}),
        )
