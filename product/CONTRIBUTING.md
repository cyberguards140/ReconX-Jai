# Contributing to ReconX

Thank you for your interest in contributing to ReconX!

## Getting Started
1. Fork the repository on GitHub.
2. Clone your fork locally.
3. Install development dependencies:
   ```bash
   pip install -e .[dev]
   ```

## Development Workflow
1. Create a branch from `develop`:
   ```bash
   git checkout -b feature/my-new-feature
   ```
2. Write your code and tests.
3. Validate locally:
   ```bash
   ruff check .
   pytest
   ```
4. Push your branch and open a Pull Request against `develop`.

## Coding Standards
- We strictly utilize `black` formatting styles (enforced by `ruff`).
- Business logic MUST be placed inside `src/reconx/services/`.
- Do not bypass `EventBus` for audit-logging events.
- Typer CLI commands MUST utilize `rich` tables and progress bars.
