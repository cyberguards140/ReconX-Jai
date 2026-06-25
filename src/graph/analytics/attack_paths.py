import logging
from typing import Any

from neo4j import AsyncDriver

from graph.neo4j.connection import get_neo4j_driver

logger = logging.getLogger(__name__)


class AttackPathAnalyzer:
    def __init__(self, driver: AsyncDriver = None):
        self._driver = driver

    async def get_driver(self) -> AsyncDriver:
        if not self._driver:
            self._driver = await get_neo4j_driver()
        return self._driver

    async def find_shortest_path(
        self, start_id: str, end_id: str, max_depth: int = 5
    ) -> list[dict[str, Any]]:
        """
        Finds the shortest path between two nodes up to max_depth.
        """
        driver = await self.get_driver()
        query = (
            """
        MATCH (start {id: $start_id}), (end {id: $end_id})
        MATCH path = shortestPath((start)-[*.."""
            + str(int(max_depth))
            + """]-(end))
        RETURN nodes(path) AS nodes, relationships(path) AS relationships
        """
        )

        paths = []
        async with driver.session() as session:
            try:
                result = await session.run(query, start_id=start_id, end_id=end_id)
                async for record in result:
                    nodes = [{"id": n["id"], "labels": list(n.labels)} for n in record["nodes"]]
                    rels = [
                        {"type": r.type, "start": r.start_node["id"], "end": r.end_node["id"]}
                        for r in record["relationships"]
                    ]
                    paths.append({"nodes": nodes, "relationships": rels})
            except Exception as e:
                logger.error(f"Failed to calculate shortest path: {e}")

        return paths

    async def find_exposure_paths(
        self, target_asset_id: str, max_depth: int = 5
    ) -> list[dict[str, Any]]:
        """
        Finds paths from any known ThreatActor or IOC to a target asset.
        """
        driver = await self.get_driver()
        query = (
            """
        MATCH (target:Asset {id: $target_id})
        MATCH (threat) WHERE threat:ThreatActor OR threat:IOC
        MATCH path = shortestPath((threat)-[*.."""
            + str(int(max_depth))
            + """]->(target))
        RETURN nodes(path) AS nodes, relationships(path) AS relationships
        """
        )

        paths = []
        async with driver.session() as session:
            try:
                result = await session.run(query, target_id=target_asset_id)
                async for record in result:
                    nodes = [{"id": n["id"], "labels": list(n.labels)} for n in record["nodes"]]
                    rels = [
                        {"type": r.type, "start": r.start_node["id"], "end": r.end_node["id"]}
                        for r in record["relationships"]
                    ]
                    paths.append({"nodes": nodes, "relationships": rels})
            except Exception as e:
                logger.error(f"Failed to calculate exposure paths: {e}")

        return paths

    async def identify_chokepoints(self, target_project_id: str) -> list[dict[str, Any]]:
        """
        Identifies nodes that many attack paths traverse through (high in-degree centralities).
        """
        driver = await self.get_driver()
        query = """
        MATCH (a:Asset {project_id: $project_id})-[r]->(b:Asset)
        WITH b, count(r) AS inbound_paths
        WHERE inbound_paths > 5
        RETURN b.id AS id, b.value AS value, inbound_paths
        ORDER BY inbound_paths DESC LIMIT 20
        """
        chokepoints = []
        async with driver.session() as session:
            try:
                result = await session.run(query, project_id=target_project_id)
                async for record in result:
                    chokepoints.append(
                        {
                            "id": record["id"],
                            "value": record["value"],
                            "inbound_paths": record["inbound_paths"],
                        }
                    )
            except Exception as e:
                logger.error(f"Failed to calculate chokepoints: {e}")
        return chokepoints

    async def map_blast_radius(
        self, start_asset_id: str, max_depth: int = 3
    ) -> list[dict[str, Any]]:
        """
        Computes all downstream assets impacted if the start asset is compromised.
        """
        driver = await self.get_driver()
        query = (
            """
        MATCH (start:Asset {id: $start_id})-[*1.."""
            + str(int(max_depth))
            + """]->(impacted:Asset)
        RETURN DISTINCT impacted.id AS id, impacted.value AS value, labels(impacted) AS labels
        """
        )
        impacted = []
        async with driver.session() as session:
            try:
                result = await session.run(query, start_id=start_asset_id)
                async for record in result:
                    impacted.append(
                        {"id": record["id"], "value": record["value"], "labels": record["labels"]}
                    )
            except Exception as e:
                logger.error(f"Failed to calculate blast radius: {e}")
        return impacted

    async def find_high_risk_chains(self, project_id: str) -> list[dict[str, Any]]:
        """
        Identifies multi-stage attack paths from public assets to internal/critical assets.
        e.g., (Public IP) -> (Vulnerable Service) -> (Internal Subnet)
        """
        driver = await self.get_driver()
        # Find paths starting from any node with 'Public' exposure tag and ending at 'Critical' tag
        query = """
        MATCH path = (start:Asset)-[*1..4]->(target:Asset)
        WHERE 'public' IN start.exposure_tags AND 'critical' IN target.exposure_tags
        AND start.project_id = $project_id
        RETURN nodes(path) AS nodes, relationships(path) AS relationships
        LIMIT 50
        """
        chains = []
        async with driver.session() as session:
            try:
                result = await session.run(query, project_id=project_id)
                async for record in result:
                    nodes = [
                        {
                            "id": n["id"],
                            "labels": list(n.labels),
                            "tags": n.get("exposure_tags", []),
                        }
                        for n in record["nodes"]
                    ]
                    rels = [
                        {"type": r.type, "start": r.start_node["id"], "end": r.end_node["id"]}
                        for r in record["relationships"]
                    ]
                    chains.append({"nodes": nodes, "relationships": rels})
            except Exception as e:
                logger.error(f"Failed to calculate high-risk chains: {e}")
        return chains
