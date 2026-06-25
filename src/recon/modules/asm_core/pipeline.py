import logging
from typing import Any

from recon.modules.asm_core.correlation import CorrelationEngine
from recon.modules.asm_core.enrichment import EnrichmentEngine
from recon.modules.asm_core.ingest_engine import IngestEngine
from recon.modules.asm_core.validation import AbstractValidationLayer

logger = logging.getLogger(__name__)


class ASMOrchestrator:
    """
    ASM Pipeline Orchestrator
    Flow: Ingest -> Normalize -> Validate -> Enrich -> Correlate
    """

    def __init__(self):
        self.ingest_engine = IngestEngine()
        self.validation_layer = AbstractValidationLayer()
        self.enrichment_engine = EnrichmentEngine()
        self.correlation_engine = CorrelationEngine()

    def process_records(self, records: list[dict[str, Any]], source: str) -> dict[str, Any]:
        """
        Process a batch of records through the entire ASM pipeline.
        """
        results = {"assets": [], "validation_signals": [], "correlation_edges": []}

        # 1. Ingest & Normalize
        assets = self.ingest_engine.ingest_records(records, source)

        for asset in assets:
            # 2. Validate
            val_signal = self.validation_layer.validate_asset(asset)
            results["validation_signals"].append(val_signal)

            # 3. Enrich
            enriched_asset = self.enrichment_engine.process(asset)
            results["assets"].append(enriched_asset)

            # 4. Correlate
            edges = self.correlation_engine.correlate(enriched_asset)
            results["correlation_edges"].extend(edges)

            # Add to correlation cache for future records
            self.correlation_engine.add_to_cache(enriched_asset)

        logger.info(
            f"Processed {len(records)} records from {source}. Yielded {len(assets)} normalized assets."
        )
        return results
