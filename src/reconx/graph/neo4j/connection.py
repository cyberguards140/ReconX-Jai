import os
import logging
from neo4j import AsyncGraphDatabase, AsyncDriver
from typing import Optional

logger = logging.getLogger(__name__)

class Neo4jConnectionManager:
    def __init__(self):
        self._driver: Optional[AsyncDriver] = None
        self._uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
        self._user = os.getenv("NEO4J_USER", "neo4j")
        self._password = os.getenv("NEO4J_PASSWORD", "password")

    async def connect(self):
        if not self._driver:
            try:
                self._driver = AsyncGraphDatabase.driver(
                    self._uri, 
                    auth=(self._user, self._password),
                    max_connection_lifetime=3600,
                    max_connection_pool_size=50,
                    connection_acquisition_timeout=60.0
                )
                await self._driver.verify_connectivity()
                logger.info("Successfully connected to Neo4j database.")
            except Exception as e:
                logger.warning(f"Neo4j is currently unreachable at {self._uri}: {e}. Will retry upon query.")

    async def close(self):
        if self._driver:
            await self._driver.close()
            self._driver = None
            logger.info("Neo4j connection closed.")

    def get_driver(self) -> AsyncDriver:
        if not self._driver:
            raise RuntimeError("Neo4j driver is not initialized. Call connect() first.")
        return self._driver

# Singleton instance
neo4j_manager = Neo4jConnectionManager()

async def get_neo4j_driver() -> AsyncDriver:
    return neo4j_manager.get_driver()

async def init_neo4j():
    await neo4j_manager.connect()

async def close_neo4j():
    await neo4j_manager.close()
