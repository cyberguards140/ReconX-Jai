import logging
import os

logger = logging.getLogger(__name__)


class ServiceRegistry:
    """
    Internal Service Discovery mechanism.
    In a Kubernetes environment, this mostly wraps K8s DNS resolution,
    but provides a unified interface for service-to-service calls.
    """

    # Defaults mapping logical service names to K8s DNS or local Docker compose names
    _registry: dict[str, str] = {
        "auth-service": os.getenv("AUTH_SERVICE_URL", "http://auth-service:8000"),
        "asset-service": os.getenv("ASSET_SERVICE_URL", "http://asset-service:8000"),
        "workflow-service": os.getenv("WORKFLOW_SERVICE_URL", "http://workflow-service:8000"),
        "graph-service": os.getenv("GRAPH_SERVICE_URL", "http://graph-service:8000"),
        "gateway": os.getenv("API_GATEWAY_URL", "http://api-gateway:8000"),
    }

    @classmethod
    def get_service_url(cls, service_name: str) -> str:
        """Resolves a logical service name to its network endpoint."""
        url = cls._registry.get(service_name)
        if not url:
            raise ValueError(f"Service '{service_name}' not found in registry.")
        return url

    @classmethod
    def register_service(cls, service_name: str, url: str):
        """Allows dynamic registration of endpoints (useful for non-K8s deployments)."""
        cls._registry[service_name] = url
        logger.info(f"Registered service {service_name} at {url}")
