from typing import Any

from recon.modules.asm_core.normalization import NormalizationEngine
from recon.modules.asm_core.schema import UnifiedAsset


class IngestEngine:
    def __init__(self):
        self.normalization_engine = NormalizationEngine()

    def ingest_records(self, records: list[dict[str, Any]], source: str) -> list[UnifiedAsset]:
        """Ingest a list of raw records and normalize them."""
        normalized_assets = []
        for record in records:
            asset = self.normalization_engine.normalize(record, source)
            normalized_assets.append(asset)
        return normalized_assets

    def ingest_stream(self, stream, source: str):
        """Generator to ingest and normalize records from a stream."""
        for record in stream:
            yield self.normalization_engine.normalize(record, source)
