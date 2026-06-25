# Changelog

All notable changes to this project will be documented in this file.
The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [4.0.0] - 2026-06-17

### Added
- Centralized Service Layer separating logic from presentation modules.
- Strictly validated `StandardResponse` JSON formatting across the entire FastAPI layer.
- `CorrelationMiddleware` and `ResponseTimingMiddleware` for request tracking.
- `structlog` implementation for structured JSON logging in production environments.
- Comprehensive Typer CLI UX overhaul utilizing `rich` progress bars and tables.
- Official Docker (`Dockerfile`) and Docker Compose definitions for production stack parity.
- `backup.sh` and `restore.sh` disaster recovery utilities.
- GitHub Actions pipeline (`ci.yml`) enforcing `ruff`, `pytest`, and `mypy` static validations.

### Changed
- Event architecture decoupled into `EventBus` with dedicated `Handlers`.
- Workflow and Plugin orchestration consolidated into explicit `workflow_service` and `plugin_service` singletons.
- Shifted default SQLite instantiation into explicit Database abstraction modules compatible with `asyncpg` architectures.

### Removed
- Legacy hardcoded environment assumptions and duplicate plugin loop configurations.
- Unstructured console output blocks across CLI routes.
