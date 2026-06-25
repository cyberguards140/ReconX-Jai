import logging
from typing import Dict, Any
from neo4j import AsyncDriver
from reconx.graph.neo4j.connection import get_neo4j_driver

logger = logging.getLogger(__name__)

class RiskPropagationEngine:
    def __init__(self, driver: AsyncDriver = None):
        self._driver = driver

    async def get_driver(self) -> AsyncDriver:
        if not self._driver:
            self._driver = await get_neo4j_driver()
        return self._driver

    async def propagate_risk(self, tenant_id: str, max_depth: int = 3) -> Dict[str, Any]:
        """
        Calculates and propagates risk scores across connected assets.
        This uses a simplified PageRank-style propagation where risk flows along 'CONNECTED_TO' or 'DEPENDS_ON' edges.
        """
        driver = await self.get_driver()
        
        # In a real scenario, we might use Neo4j Graph Data Science (GDS) library.
        # For this foundation, we calculate a simple risk score increment based on 1-hop exposure to ThreatActor or IOCs.
        query = """
        MATCH (asset:Asset {tenant_id: $tenant_id})
        OPTIONAL MATCH (asset)<-[*1..2]-(threat) WHERE threat:ThreatActor OR threat:IOC
        WITH asset, count(threat) as threat_count
        SET asset.risk_score = coalesce(asset.base_risk, 0) + (threat_count * 10)
        RETURN asset.id as id, asset.risk_score as risk_score
        """
        
        results = {}
        async with driver.session() as session:
            try:
                res = await session.run(query, tenant_id=tenant_id)
                async for record in res:
                    results[record["id"]] = record["risk_score"]
            except Exception as e:
                logger.error(f"Failed to propagate risk for tenant {tenant_id}: {e}")
                
        return results
