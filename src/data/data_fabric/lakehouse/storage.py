import logging
from typing import Any

from plugins.enterprise.isolation.tenant_context import get_current_tenant_id

logger = logging.getLogger(__name__)


class LakehouseStorage:
    """
    Abstracts interactions with the underlying Data Lake (Parquet/Delta/Iceberg).
    Provides Immutable Historical Records partitioned by tenant.
    """

    def __init__(self):
        # In a real environment, this would manage AWS S3/GCS blob paths and PyArrow/Delta table references
        self._mock_storage = []

    def commit_records(self, domain: str, records: list[dict[str, Any]]) -> bool:
        """
        Appends data to the lakehouse domain (e.g., 'assets', 'incidents').
        """
        tenant_id = get_current_tenant_id() or "system"
        logger.info(
            f"Committing {len(records)} records to lakehouse domain: {domain} for tenant {tenant_id}"
        )

        # Enforce tenant isolation structurally
        for record in records:
            record["_tenant_id"] = tenant_id
            record["_domain"] = domain
            self._mock_storage.append(record)

        return True

    def query_records(self, domain: str, limit: int = 100) -> list[dict[str, Any]]:
        """
        Retrieves historical records for a specific domain.
        """
        tenant_id = get_current_tenant_id() or "system"
        return [
            r for r in self._mock_storage if r["_tenant_id"] == tenant_id and r["_domain"] == domain
        ][:limit]


lakehouse_storage = LakehouseStorage()
