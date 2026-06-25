from typing import Any

from recon.modules.infra_intel.schema import (
    InfraEntityModel,
)


class InfraCorrelationEngine:
    """
    Correlation logic for Infrastructure entities.
    Links Asset IPs to Netblocks, ASNs to Organizations, and Certs to Domains.
    """

    def __init__(self):
        self.node_cache = {}

    def add_node(self, node: InfraEntityModel):
        self.node_cache[node.id] = node

    def correlate(self, node: InfraEntityModel) -> list[dict[str, Any]]:
        """
        Determine relationship edges for the node.
        Relationships: ANNOUNCES, OWNS, HOSTS, SIGNED_BY, BELONGS_TO.
        """
        edges = []
        for cached_id, cached_node in self.node_cache.items():
            if cached_id == node.id:
                continue

            # ASN -> Netblock = ANNOUNCES
            if node.entity_type == "netblock" and cached_node.entity_type == "asn":
                if node.owner_asn == cached_node.value:
                    edges.append(
                        {"source": cached_id, "target": node.id, "relationship": "ANNOUNCES"}
                    )

            # Organization -> ASN/Netblock = OWNS
            if (
                node.entity_type in ("asn", "netblock")
                and cached_node.entity_type == "organization"
            ):
                if node.id in cached_node.infrastructure:
                    edges.append({"source": cached_id, "target": node.id, "relationship": "OWNS"})

            # Certificate -> Domain = SIGNED_BY
            if node.entity_type == "certificate" and cached_node.entity_type == "organization":
                # Conceptually: cached_node could be domain asset, here it's simplified.
                for domain in node.domains:
                    if domain in cached_node.domains:
                        edges.append(
                            {"source": node.id, "target": cached_id, "relationship": "SIGNED_BY"}
                        )

        return edges
