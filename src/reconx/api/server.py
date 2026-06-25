"""ReconX API server launcher."""

import uvicorn
from fastapi import FastAPI

app = FastAPI(
    title="ReconX API",
    description="Enterprise Security Reconnaissance Platform",
    version="4.0.0",
)


def start_server(port: int = 8000) -> None:
    """Start the ReconX API server."""
    uvicorn.run(
        "reconx.api.server:app",
        host="0.0.0.0",  # noqa: S104
        port=port,
        reload=False,
    )
