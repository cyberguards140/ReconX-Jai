import hashlib
import logging
from typing import Any

from data.data_fabric.lakehouse.storage import lakehouse_storage

logger = logging.getLogger(__name__)


class IngestionPipeline:
    """
    Normalizes streaming and batch data (from Kafka, APIs, Neo4j) and deduplicates
    entries before committing them to the Lakehouse.
    """

    def __init__(self):
        pass

    def _generate_fingerprint(self, record: dict[str, Any]) -> str:
        """Generates a stable hash for deduplication based on core data."""
        # A real implementation would filter out ephemeral timestamps before hashing
        core_string = str(sorted(record.items()))
        return hashlib.sha256(core_string.encode("utf-8")).hexdigest()

    def process_batch(self, domain: str, raw_records: list[dict[str, Any]]) -> dict[str, Any]:
        """
        Validates, normalizes, deduplicates, and commits a batch of records.
        """
        logger.info(f"Ingestion Pipeline processing batch for domain '{domain}'")

        normalized = []
        seen_hashes = set()

        for rec in raw_records:
            fingerprint = self._generate_fingerprint(rec)
            if fingerprint not in seen_hashes:
                seen_hashes.add(fingerprint)
                # Normalization logic goes here (e.g., standardizing IP formats, flattening JSON)
                rec["_fabric_hash"] = fingerprint
                normalized.append(rec)

        # Commit to Lakehouse
        success = lakehouse_storage.commit_records(domain, normalized)

        return {
            "status": "success" if success else "failed",
            "records_received": len(raw_records),
            "records_committed": len(normalized),
            "duplicates_dropped": len(raw_records) - len(normalized),
        }


ingestion_pipeline = IngestionPipeline()
