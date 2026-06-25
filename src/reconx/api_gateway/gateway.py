from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

from reconx.api_gateway.exceptions import setup_exception_handlers
from reconx.api_gateway.router_registry import registry
from reconx.api_gateway.versioning import VersioningConfig


def configure_gateway(app: FastAPI) -> FastAPI:
    """
    Configures an existing FastAPI application to act as the API Gateway.
    Applies exception handlers, standard routing, and OpenAPI configurations.
    """
    # Setup Exception Handlers
    setup_exception_handlers(app)

    # Register all module routers dynamically based on versioning config
    for router, prefix, version, tags in registry.get_routers():
        if version in VersioningConfig.supported_versions:
            full_prefix = f"/api/{version}{prefix}"
            app.include_router(router, prefix=full_prefix, tags=tags)

    # Customize OpenAPI for 3.1.0 compatibility and rich SDK generation support
    def custom_openapi():
        if app.openapi_schema:
            return app.openapi_schema
        openapi_schema = get_openapi(
            title="ReconX API Platform",
            version="3.0.0",
            openapi_version="3.1.0",
            description="Centralized API platform for all ReconX intelligence services.",
            routes=app.routes,
        )
        app.openapi_schema = openapi_schema
        return app.openapi_schema

    app.openapi = custom_openapi  # type: ignore[method-assign]

    return app
