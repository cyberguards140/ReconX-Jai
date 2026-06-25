from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from reconx.database.config import DATABASE_URL

engine = create_async_engine(
    DATABASE_URL, 
    echo=False, 
    future=True,
    pool_pre_ping=True,
    pool_size=20 if "postgresql" in DATABASE_URL else 5,
    max_overflow=40 if "postgresql" in DATABASE_URL else 10,
)

# Apply global tenant isolation rules
from reconx.enterprise.isolation.query_filter import setup_query_filters
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
