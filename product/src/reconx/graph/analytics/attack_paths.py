import logging
from typing import List, Dict, Any
from neo4j import AsyncDriver
from reconx.graph.neo4j.connection import get_neo4j_driver

logger = logging.getLogger(__name__)

class AttackPathAnalyzer:
    def __init__(self, driver: AsyncDriver = None):
        self._driver = driver

    async def get_driver(self) -> AsyncDriver:
        if not self._driver:
            self._driver = await get_neo4j_driver()
        return self._driver

    async def find_shortest_path(self, start_id: str, end_id: str, max_depth: int = 5) -> List[Dict[str, Any]]:
        """
        Finds the shortest path between two nodes up to max_depth.
        """
        driver = await self.get_driver()
        query = """
        MATCH (start {id: $start_id}), (end {id: $end_id})
        MATCH path = shortestPath((start)-[*..""" + str(int(max_depth)) + """]-(end))
        RETURN nodes(path) AS nodes, relationships(path) AS relationships
        """
        
        paths = []
        async with driver.session() as session:
            try:
                result = await session.run(query, start_id=start_id, end_id=end_id)
                async for record in result:
                    nodes = [{"id": n["id"], "labels": list(n.labels)} for n in record["nodes"]]
                    rels = [{"type": r.type, "start": r.start_node["id"], "end": r.end_node["id"]} for r in record["relationships"]]
                    paths.append({"nodes": nodes, "relationships": rels})
            except Exception as e:
                logger.error(f"Failed to calculate shortest path: {e}")
        
        return paths

    async def find_exposure_paths(self, target_asset_id: str, max_depth: int = 5) -> List[Dict[str, Any]]:
        """
        Finds paths from any known ThreatActor or IOC to a target asset.
        """
        driver = await self.get_driver()
        query = """
        MATCH (target:Asset {id: $target_id})
        MATCH (threat) WHERE threat:ThreatActor OR threat:IOC
        MATCH path = shortestPath((threat)-[*..""" + str(int(max_depth)) + """]->(target))
        RETURN nodes(path) AS nodes, relationships(path) AS relationships
        """
        
        paths = []
        async with driver.session() as session:
            try:
                result = await session.run(query, target_id=target_asset_id)
                async for record in result:
                    nodes = [{"id": n["id"], "labels": list(n.labels)} for n in record["nodes"]]
                    rels = [{"type": r.type, "start": r.start_node["id"], "end": r.end_node["id"]} for r in record["relationships"]]
                    paths.append({"nodes": nodes, "relationships": rels})
            except Exception as e:
                logger.error(f"Failed to calculate exposure paths: {e}")
        
        return paths
