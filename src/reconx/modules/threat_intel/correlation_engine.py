from reconx.modules.asm_core.schema import UnifiedAsset
from reconx.modules.threat_intel.schema import ThreatContext
from reconx.modules.threat_intel.ioc_engine import IOCEngine
from reconx.modules.threat_intel.actor_mapper import ThreatActorMapper
from reconx.modules.threat_intel.vulnerability_linker import VulnerabilityLinker

class ThreatCorrelationEngine:
    """
    Combines Asset, IOC matches, and Vulnerability signals into a unified ThreatContext.
    """
    def __init__(self):
        self.ioc_engine = IOCEngine()
        self.actor_mapper = ThreatActorMapper()
        self.vuln_linker = VulnerabilityLinker()

    def correlate_threats(self, asset: UnifiedAsset) -> ThreatContext:
        """
        Produces a unified threat score and context mapping.
        """
        ioc_result = self.ioc_engine.match_asset(asset)
        matched_iocs = ioc_result["matched_iocs"]
        
        actor_links = self.actor_mapper.map_to_actor(matched_iocs)
        vulns = self.vuln_linker.check_vulnerabilities(asset)
        
        # Scoring logic
        risk_score = ioc_result["threat_score"]
        if actor_links:
            risk_score += 20
        if vulns:
            risk_score += 50
            
        return ThreatContext(
            ioc_matches=matched_iocs,
            actor_links=actor_links,
            risk_score=min(100, risk_score),
            confidence=asset.confidence
        )
