import time

from fastapi import HTTPException, Request


class TokenBucketRateLimiter:
    """
    Custom API Rate Limiter to protect the ReconX Gateway from abuse.
    Uses an in-memory token bucket (in production, this would use Redis).
    """

    def __init__(self, capacity: int = 100, refill_rate: float = 1.0):
        self.capacity = capacity
        self.refill_rate = refill_rate
        self.buckets: dict[str, dict[str, float]] = {}

    async def check_rate_limit(self, request: Request):
        """
        FastAPI dependency to enforce rate limits per client IP.
        """
        client_ip = request.client.host if request.client else "unknown"
        current_time = time.time()

        if client_ip not in self.buckets:
            self.buckets[client_ip] = {"tokens": self.capacity, "last_refill": current_time}

        bucket = self.buckets[client_ip]

        # Refill tokens
        time_passed = current_time - bucket["last_refill"]
        bucket["tokens"] = min(self.capacity, bucket["tokens"] + time_passed * self.refill_rate)
        bucket["last_refill"] = current_time

        # Check limit
        if bucket["tokens"] < 1:
            raise HTTPException(
                status_code=429, detail="Too Many Requests. ReconX API rate limit exceeded."
            )

        bucket["tokens"] -= 1


# Global instance for injection
rate_limiter = TokenBucketRateLimiter(
    capacity=100, refill_rate=2.0
)  # 100 requests burst, 2 requests/sec refill
