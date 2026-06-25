import time

from fastapi import Request
from prometheus_client import Counter, Histogram
from starlette.middleware.base import BaseHTTPMiddleware

from reconx.enterprise.isolation.tenant_context import get_current_tenant_id

# Define Prometheus Metrics
REQUEST_COUNT = Counter(
    "reconx_http_requests_total",
    "Total HTTP requests to the ReconX API",
    ["method", "endpoint", "status_code", "tenant_id"],
)

REQUEST_LATENCY = Histogram(
    "reconx_http_request_duration_seconds",
    "HTTP request latency in seconds",
    ["method", "endpoint", "tenant_id"],
)


class PrometheusMetricsMiddleware(BaseHTTPMiddleware):
    """
    FastAPI Middleware that collects standard RED (Rate, Errors, Duration) metrics.
    Tenant-aware for SaaS billing/capacity monitoring.
    """

    async def dispatch(self, request: Request, call_next):
        method = request.method
        # We use the raw path or route path if available, but be careful of cardinality explosion
        # (e.g. /users/123 -> /users/{id}). FastAPI request.scope["route"] requires access post-routing.
        # For simplicity, we fallback to request.url.path but in production you'd extract the matched route.
        endpoint = request.url.path

        start_time = time.time()

        try:
            response = await call_next(request)
            status_code = str(response.status_code)
            return response
        except Exception as e:
            status_code = "500"
            raise e
        finally:
            process_time = time.time() - start_time
            tenant_id = get_current_tenant_id() or "system"

            # Record Metrics
            REQUEST_COUNT.labels(
                method=method, endpoint=endpoint, status_code=status_code, tenant_id=tenant_id
            ).inc()

            REQUEST_LATENCY.labels(method=method, endpoint=endpoint, tenant_id=tenant_id).observe(
                process_time
            )
