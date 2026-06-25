import asyncio
import time

from reconx.database.base import BaseModel
from reconx.database.models import User
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

# This will benchmark the provided database URL.
# Usage: PYTHONPATH=src python scripts/db_benchmark.py [sqlite|postgres]


async def run_benchmark(db_url: str):
    print(f"Benchmarking against {db_url}...")
    engine = create_async_engine(db_url, future=True, echo=False)

    async with engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.create_all)

    SessionLocal = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

    sizes = [100, 1000, 10000]

    for size in sizes:
        start_time = time.time()

        async with SessionLocal() as session:
            for i in range(size):
                user = User(
                    username=f"user_{size}_{i}_{time.time()}",
                    email=f"user_{size}_{i}_{time.time()}@example.com",
                    password_hash="hash",
                )
                session.add(user)
            await session.commit()

        elapsed = time.time() - start_time
        print(f"  Inserted {size} records in {elapsed:.4f} seconds.")

    async with engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.drop_all)
    await engine.dispose()


if __name__ == "__main__":
    import sys

    db_type = sys.argv[1] if len(sys.argv) > 1 else "sqlite"

    if db_type == "sqlite":
        url = "sqlite+aiosqlite:///:memory:"
    else:
        # Require postgres running, e.g. postgresql+asyncpg://postgres:postgres@localhost:5432/reconx
        url = "postgresql+asyncpg://postgres:postgres@localhost:5432/reconx"

    asyncio.run(run_benchmark(url))
