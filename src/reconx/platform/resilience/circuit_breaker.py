import logging
import time
from collections.abc import Callable
from functools import wraps

logger = logging.getLogger(__name__)


class CircuitBreakerOpenException(Exception):
    pass


class CircuitBreaker:
    """
    Stateful Circuit Breaker to protect the platform from cascading failures
    when external services (e.g., APIs, databases) become unavailable.
    """

    def __init__(self, failure_threshold: int = 5, recovery_timeout: int = 60):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.failure_count = 0
        self.last_failure_time = 0
        self.state = "CLOSED"  # CLOSED, OPEN, HALF_OPEN

    def __call__(self, func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            self._check_state()

            if self.state == "OPEN":
                logger.warning(f"Circuit Breaker is OPEN. Blocking execution of {func.__name__}")
                # You might return a fallback response here instead of raising
                raise CircuitBreakerOpenException("Service temporarily unavailable")

            try:
                result = await func(*args, **kwargs)
                self._record_success()
                return result
            except Exception as e:
                self._record_failure()
                raise e

        return wrapper

    def _check_state(self):
        if self.state == "OPEN":
            if time.time() - self.last_failure_time > self.recovery_timeout:
                self.state = "HALF_OPEN"
                logger.info("Circuit Breaker transitioned to HALF_OPEN")

    def _record_success(self):
        if self.state == "HALF_OPEN":
            self.state = "CLOSED"
            self.failure_count = 0
            logger.info("Circuit Breaker recovered and transitioned to CLOSED")
        elif self.state == "CLOSED":
            self.failure_count = 0

    def _record_failure(self):
        self.failure_count += 1
        self.last_failure_time = time.time()

        if self.state == "HALF_OPEN" or self.failure_count >= self.failure_threshold:
            self.state = "OPEN"
            logger.error("Circuit Breaker tripped and transitioned to OPEN")


# Global instances for key external dependencies
db_circuit_breaker = CircuitBreaker(failure_threshold=10, recovery_timeout=30)
kafka_circuit_breaker = CircuitBreaker(failure_threshold=5, recovery_timeout=60)
redis_circuit_breaker = CircuitBreaker(failure_threshold=5, recovery_timeout=15)
