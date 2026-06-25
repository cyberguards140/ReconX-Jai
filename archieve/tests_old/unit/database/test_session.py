import pytest
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from reconx.database.base import BaseModel

@pytest.fixture
async def async_db():
    engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.create_all)
    
    SessionLocal = async_sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )
    
    async with SessionLocal() as session:
        yield session

@pytest.mark.asyncio
async def test_session_creation(async_db):
    assert async_db is not None
    assert async_db.is_active

@pytest.mark.asyncio
async def test_crud_operations(async_db):
    # This is a generic test placeholder to verify the session works.
    # Replace with an actual model query when available.
    pass
