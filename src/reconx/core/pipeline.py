"""Core pipeline module for ReconX."""

from typing import Any


class IngestionPipeline:
    """Pipeline for ingesting and processing scan results into the database."""

    def __init__(self, db: Any):
        self.db = db

    async def ingest(self, results: dict) -> None:
        """Ingest raw scan results into the normalized database."""
        # TODO: Implement full ingestion logic
        pass
