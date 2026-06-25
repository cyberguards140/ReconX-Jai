# Deployment Guide

ReconX supports local installation via `pip` and containerized deployments via `Docker`.

## Docker Compose (Recommended)

To deploy the entire stack including the background PostgreSQL database:
```bash
docker-compose up -d --build
```

The API will be available at `http://localhost:8000`.

## Standalone Docker

To build and run just the ReconX image (e.g., pointing it to an external database via ENV variables):
```bash
docker build -t reconx:4.0.0 .
docker run -p 8000:8000 -e DATABASE_URL="postgresql+asyncpg://..." reconx:4.0.0
```

## Local Python Environment

For development or direct shell access:
```bash
python -m venv venv
source venv/bin/activate
pip install .
reconx version
```

## Kubernetes (Beta)
The `/health/ready` probe has been enabled for Kubernetes integration. Ensure that persistent volumes are mounted for `/app/data` (SQLite) and `/app/logs` if not utilizing centralized observability stacks.
