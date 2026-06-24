# Release Process

ReconX uses a Gitflow-inspired branching strategy.

## Branches

- **`main`**: The production-ready branch. Code here is always deployable and maps to official PyPI/Docker tags.
- **`develop`**: The integration branch for active development.
- **`release/vX.X`**: Branched from `develop` when preparing for a new release. Used solely for stabilization, bug fixes, and documentation.
- **`hotfix/*`**: Branched from `main` to address critical production issues. Merges back to both `main` and `develop`.

## Semantic Versioning

We strictly adhere to `MAJOR.MINOR.PATCH`:
- **MAJOR**: Incompatible API changes, major architectural rewrites (e.g., v3.0 -> v4.0).
- **MINOR**: Backward-compatible new features (e.g., v4.0 -> v4.1).
- **PATCH**: Backward-compatible bug fixes (e.g., v4.1.0 -> v4.1.1).

## Performing a Release
1. Create a `release/vX.X.X` branch from `develop`.
2. Bump versions in `pyproject.toml` and `__init__.py`.
3. Complete the `docs/release-checklist.md`.
4. Open a PR against `main`.
5. Upon merge, tag the commit with `vX.X.X` and push to remote.
6. Automation will build the PyPI package and Docker image.
