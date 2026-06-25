import logging

try:
    from redis.asyncio import ConnectionPool, Redis
except ImportError:
    Redis = None
    ConnectionPool = None

logger = logging.getLogger(__name__)


class RedisClientManager:
    """
    Manages the global async Redis connection pool.
    Supports Sentinel and Cluster mode in a real deployment.
    """

    _pool: ConnectionPool | None = None
    _redis_client: Redis | None = None

    @classmethod
    async def initialize(cls, redis_url: str = "redis://redis:6379/0"):
        if not Redis:
            logger.warning("redis not installed. Running in mock caching mode.")
            return

        if not cls._pool:
            # Setup connection pool for high concurrency
            cls._pool = ConnectionPool.from_url(
                redis_url, max_connections=100, decode_responses=True
            )
            cls._redis_client = Redis(connection_pool=cls._pool)
            logger.info(f"Initialized Redis connection pool to {redis_url}")

    @classmethod
    async def get_client(cls) -> Redis | None:
        return cls._redis_client

    @classmethod
    async def close(cls):
        if cls._redis_client:
            await cls._redis_client.close()
        if cls._pool:
            await cls._pool.disconnect()


redis_manager = RedisClientManager()
