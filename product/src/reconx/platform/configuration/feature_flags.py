import logging
from typing import Dict, Any

from reconx.platform.redis.client import redis_manager

logger = logging.getLogger(__name__)

class FeatureFlagManager:
    """
    Distributed Feature Flag System for ReconX.
    Allows enabling/disabling features globally or per-tenant at runtime.
    """
    
    # In-memory fallback if Redis is down
    _local_cache: Dict[str, bool] = {
        "global:enable_kafka": True,
        "global:enable_distributed_workflows": True,
        "global:beta_analytics": False
    }

    @classmethod
    async def is_enabled(cls, feature_name: str, tenant_id: str = "global") -> bool:
        client = await redis_manager.get_client()
        key = f"fflag:{tenant_id}:{feature_name}"
        
        if client:
            try:
                val = await client.get(key)
                if val is not None:
                    return val == "1" or val.lower() == "true"
            except Exception as e:
                logger.debug(f"Redis feature flag check failed: {e}")

        # Fallback to local cache (first tenant-specific, then global)
        local_key_tenant = f"{tenant_id}:{feature_name}"
        local_key_global = f"global:{feature_name}"
        
        if local_key_tenant in cls._local_cache:
            return cls._local_cache[local_key_tenant]
            
        return cls._local_cache.get(local_key_global, False)

    @classmethod
    async def set_flag(cls, feature_name: str, enabled: bool, tenant_id: str = "global"):
        """Runtime updates to feature flags."""
        client = await redis_manager.get_client()
        key = f"fflag:{tenant_id}:{feature_name}"
        val = "1" if enabled else "0"
        
        if client:
            try:
                await client.set(key, val)
                logger.info(f"Feature flag {key} set to {enabled}")
            except Exception as e:
                logger.error(f"Failed to set feature flag in Redis: {e}")
        
        # Always update local cache
        local_key = f"{tenant_id}:{feature_name}"
        cls._local_cache[local_key] = enabled
