import asyncio
import time

from fastapi import Request

from reconx.api_gateway.exceptions import RateLimitException

# Simple in-memory sliding window rate limiter fallback
# Dict[client_id, list of timestamps]
_memory_store: dict[str, list[float]] = {}
_store_lock = asyncio.Lock()


class RateLimiter:
    def __init__(self, requests: int = 100, window_seconds: int = 60):
        self.requests = requests
        self.window_seconds = window_seconds

    async def __call__(self, request: Request):
        # Determine client identifier (user_id or IP)
        identity = getattr(request.state, "identity", None)
        if identity and identity.user_id:
            client_id = f"user:{identity.user_id}"
        else:
            client_id = f"ip:{request.client.host if request.client else 'unknown'}"

        now = time.time()

        async with _store_lock:
            if client_id not in _memory_store:
                _memory_store[client_id] = []

            # Clean up old timestamps
            _memory_store[client_id] = [
                t for t in _memory_store[client_id] if now - t < self.window_seconds
            ]

            if len(_memory_store[client_id]) >= self.requests:
                raise RateLimitException(message="Rate limit exceeded. Please try again later.")

            _memory_store[client_id].append(now)


# Default rate limiter: 100 requests per minute
rate_limiter = RateLimiter(requests=100, window_seconds=60)
