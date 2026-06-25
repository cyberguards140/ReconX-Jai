import logging
from typing import Any

logger = logging.getLogger(__name__)


class CertificateGraphEngine:
    """
    Phase 65: Global Certificate Intelligence.
    Maps SSL/TLS Certificate ownership, trust chains, and SAN records.
    """

    def __init__(self):
        pass

    def build_trust_chain(self, cert_data: dict[str, Any]) -> list[dict[str, Any]]:
        """
        Extracts edges for Neo4j: (Domain)-[:USES]->(Certificate)-[:ISSUED_BY]->(Issuer).
        """
        domain = cert_data.get("domain")
        common_name = cert_data.get("common_name")
        issuer = cert_data.get("issuer")

        edges = []
        if domain and common_name:
            edges.append({"source": domain, "relation": "USES", "target": common_name})
        if common_name and issuer:
            edges.append({"source": common_name, "relation": "ISSUED_BY", "target": issuer})

        # Parse Subject Alternative Names (SANs) to find hidden infrastructure
        sans = cert_data.get("subject_alternative_names", [])
        for san in sans:
            edges.append({"source": san, "relation": "USES", "target": common_name})

        logger.info(
            f"[Certificate Intel] Built Trust Chain for {domain}: {len(edges)} edges detected."
        )
        return edges


certificate_engine = CertificateGraphEngine()
