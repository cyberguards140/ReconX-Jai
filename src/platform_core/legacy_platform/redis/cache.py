import hashlib
import json
import logging
from collections.abc import Callable
from functools import wraps

from platform_core.legacy_platform.redis.client import redis_manager

logger = logging.getLogger(__name__)


def cached(ttl: int = 300, key_prefix: str = "reconx:cache"):
    """
    Distributed caching decorator for async functions.
    Handles serialization and automatic cache invalidation policies via TTL.
    """

    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            client = await redis_manager.get_client()
            if not client:
                # If Redis is unavailable, fallback to direct execution (Resilience)
                return await func(*args, **kwargs)

            # Generate deterministic cache key based on function arguments
            # Note: In a true multi-tenant environment, tenant_id must be part of kwargs or args
            # or extracted from the global ContextVar. We assume safe hashing for now.
            key_data = f"{func.__module__}.{func.__name__}:{args}:{kwargs}"
            key_hash = hashlib.sha256(key_data.encode()).hexdigest()
            cache_key = f"{key_prefix}:{key_hash}"

            try:
                cached_val = await client.get(cache_key)
                if cached_val:
                    return json.loads(cached_val)
            except Exception as e:
                logger.warning(f"Cache read failed for {cache_key}: {e}")

            # Execute actual function
            result = await func(*args, **kwargs)

            try:
                if result is not None:
                    await client.setex(cache_key, ttl, json.dumps(result))
            except Exception as e:
                logger.warning(f"Cache write failed for {cache_key}: {e}")

            return result

        return wrapper

    return decorator
