import logging

from neo4j import AsyncDriver

logger = logging.getLogger(__name__)

CONSTRAINTS = [
    # Asset constraints
    "CREATE CONSTRAINT asset_id_unique IF NOT EXISTS FOR (n:Asset) REQUIRE n.id IS UNIQUE",
    "CREATE CONSTRAINT domain_name_unique IF NOT EXISTS FOR (n:Domain) REQUIRE n.name IS UNIQUE",
    "CREATE CONSTRAINT ip_address_unique IF NOT EXISTS FOR (n:IP) REQUIRE n.address IS UNIQUE",
    # Threat constraints
    "CREATE CONSTRAINT ioc_value_unique IF NOT EXISTS FOR (n:IOC) REQUIRE n.value IS UNIQUE",
    "CREATE CONSTRAINT threatactor_name_unique IF NOT EXISTS FOR (n:ThreatActor) REQUIRE n.name IS UNIQUE",
    # SOC constraints
    "CREATE CONSTRAINT alert_id_unique IF NOT EXISTS FOR (n:Alert) REQUIRE n.id IS UNIQUE",
    "CREATE CONSTRAINT incident_id_unique IF NOT EXISTS FOR (n:Incident) REQUIRE n.id IS UNIQUE",
]

INDEXES = [
    "CREATE INDEX asset_tenant_idx IF NOT EXISTS FOR (n:Asset) ON (n.tenant_id)",
    "CREATE INDEX threat_tenant_idx IF NOT EXISTS FOR (n:ThreatActor) ON (n.tenant_id)",
    "CREATE INDEX incident_tenant_idx IF NOT EXISTS FOR (n:Incident) ON (n.tenant_id)",
]


async def setup_indexes_and_constraints(driver: AsyncDriver):
    """
    Apply necessary Neo4j constraints and indexes to enforce schema integrity.
    """
    async with driver.session() as session:
        for query in CONSTRAINTS:
            try:
                await session.run(query)
            except Exception as e:
                logger.error(f"Failed to create constraint: {e}")

        for query in INDEXES:
            try:
                await session.run(query)
            except Exception as e:
                logger.error(f"Failed to create index: {e}")

    logger.info("Successfully applied graph constraints and indexes.")
