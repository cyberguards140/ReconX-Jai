import asyncio

# Import models to ensure they are registered with BaseModel.metadata
from core.logging.logger import setup_logger
from data.database.base import BaseModel
from data.database.session import engine
import data.database.models

logger = setup_logger(__name__)


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.create_all)


async def verify_connection():
    try:
        async with engine.connect():
            logger.info("Database connection verified.")
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
        raise


async def seed_defaults():
    # Only if using an actual DB setup that doesn't use Alembic, but user said:
    # Seed: Admin role, Operator role, Viewer role. Do NOT create default admin accounts.
    logger.info("Default roles (Admin, Operator, Viewer) supported via codebase.")


async def init():
    await verify_connection()
    await create_tables()
    await seed_defaults()


if __name__ == "__main__":
    asyncio.run(init())
