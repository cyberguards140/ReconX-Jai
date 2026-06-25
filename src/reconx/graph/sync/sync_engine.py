import logging
from typing import Dict, Any, Optional
from neo4j import AsyncDriver
from reconx.graph.neo4j.connection import get_neo4j_driver
from reconx.graph.schema.nodes import NodeLabel
from reconx.graph.schema.relationships import RelType

logger = logging.getLogger(__name__)

class GraphSyncEngine:
    """
    Handles synchronization of entities into Neo4j graph nodes and relationships.
    """
    def __init__(self, driver: Optional[AsyncDriver] = None):
        self._driver = driver

    async def get_driver(self) -> AsyncDriver:
        if not self._driver:
            self._driver = await get_neo4j_driver()
        return self._driver

    async def sync_node(self, label: str, node_id: str, properties: Dict[str, Any]):
        """
        Merge a node into the graph.
        """
        driver = await self.get_driver()
        query = f"""
        MERGE (n:{label} {{id: $id}})
        SET n += $props
        RETURN n
        """
        async with driver.session() as session:
            try:
                # Remove id from props as it's used in MERGE
                props = properties.copy()
                props.pop("id", None)
                await session.run(query, id=node_id, props=props)
            except Exception as e:
                logger.error(f"Failed to sync node {label}:{node_id} - {e}")

    async def sync_relationship(
        self,
        from_label: str, from_id: str,
        rel_type: str,
        to_label: str, to_id: str,
        properties: Optional[Dict[str, Any]] = None
    ):
        """
        Merge a relationship between two nodes.
        Assumes both nodes exist (or creates empty nodes with just ID if they don't).
        """
        driver = await self.get_driver()
        props = properties or {}
        query = f"""
        MERGE (a:{from_label} {{id: $from_id}})
        MERGE (b:{to_label} {{id: $to_id}})
        MERGE (a)-[r:{rel_type}]->(b)
        SET r += $props
        RETURN r
        """
        async with driver.session() as session:
            try:
                await session.run(query, from_id=from_id, to_id=to_id, props=props)
            except Exception as e:
                logger.error(f"Failed to sync relationship {from_label}:{from_id} -> {rel_type} -> {to_label}:{to_id} - {e}")

    async def remove_node(self, label: str, node_id: str):
        driver = await self.get_driver()
        query = f"""
        MATCH (n:{label} {{id: $id}})
        DETACH DELETE n
        """
        async with driver.session() as session:
            try:
                await session.run(query, id=node_id)
            except Exception as e:
                logger.error(f"Failed to remove node {label}:{node_id} - {e}")

    async def remove_relationship(
        self,
        from_label: str, from_id: str,
        rel_type: str,
        to_label: str, to_id: str
    ):
        driver = await self.get_driver()
        query = f"""
        MATCH (a:{from_label} {{id: $from_id}})-[r:{rel_type}]->(b:{to_label} {{id: $to_id}})
        DELETE r
        """
        async with driver.session() as session:
            try:
                await session.run(query, from_id=from_id, to_id=to_id)
            except Exception as e:
                logger.error(f"Failed to remove relationship - {e}")

# Global instance
sync_engine = GraphSyncEngine()
