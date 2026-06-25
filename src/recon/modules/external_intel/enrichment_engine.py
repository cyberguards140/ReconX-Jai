import logging

from recon.modules.asm_core.schema import UnifiedAsset
from recon.modules.external_intel.context_aggregator import ContextAggregator
from recon.modules.external_intel.exposure_mapper import ExposureMapper
from recon.modules.external_intel.intelligence_cache import IntelligenceCache
from recon.modules.external_intel.reputation_engine import ReputationEngine
from recon.modules.external_intel.schema import ExternalIntelModel
from recon.modules.external_intel.threat_linker import ThreatLinker

logger = logging.getLogger(__name__)


class ExternalEnrichmentEngine:
    """
    Orchestrates the exposure, reputation, and threat mapping.
    """

    def __init__(self):
        self.exposure_mapper = ExposureMapper()
        self.reputation_engine = ReputationEngine()
        self.threat_linker = ThreatLinker()
        self.context_aggregator = ContextAggregator()
        self.cache = IntelligenceCache()

    def enrich_asset(self, asset: UnifiedAsset) -> ExternalIntelModel:
        """
        Enrich an asset with external intelligence.
        """
        lookup_key = f"intel_v1_{asset.asset_type}_{asset.value}"
        cached = self.cache.get_intel(lookup_key)

        if cached:
            logger.debug(f"Cache hit for {lookup_key}")
            return ExternalIntelModel(**cached)

        exposure = self.exposure_mapper.map_exposure(asset)
        reputation = self.reputation_engine.evaluate_reputation(asset)
        threats = self.threat_linker.get_threat_tags(asset)

        intel_model = ExternalIntelModel(
            exposure=exposure,
            reputation=reputation,
            threat_indicators=threats,
            external_tags=["auto_enriched"],
        )

        self.cache.set_intel(lookup_key, intel_model.model_dump())
        return intel_model
