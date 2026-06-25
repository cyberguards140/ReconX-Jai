from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from data.database.config import DATABASE_URL

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_async_engine(
    DATABASE_URL,
    echo=False,
    future=True,
    pool_pre_ping=True,
    pool_size=20 if "postgresql" in DATABASE_URL else 5,
    max_overflow=40 if "postgresql" in DATABASE_URL else 10,
)

# Create a synchronous SessionLocal for legacy code compatibility
sync_url = DATABASE_URL.replace("+asyncpg", "").replace("+aiosqlite", "")
sync_engine = create_engine(
    sync_url,
    pool_pre_ping=True,
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=sync_engine)

# Apply global tenant isolation rules
from plugins.enterprise.isolation.query_filter import setup_query_filters

setup_query_filters(engine)

async_session_factory = async_sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
    class_=AsyncSession,
)


async def get_db():
    async with async_session_factory() as session:
        yield session
