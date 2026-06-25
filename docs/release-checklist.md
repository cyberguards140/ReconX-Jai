# Release Checklist

Ensure the following criteria are met before tagging and releasing v4.0.0.

- [ ] All automated CI tests are passing (`ruff`, `pytest`, `mypy`).
- [ ] Test coverage is maintained above the required threshold (>80%).
- [ ] `reconx version` reflects the targeted version (`4.0.0`).
- [ ] `pyproject.toml` and `src/reconx/__init__.py` versions are synced.
- [ ] Documentation (`docs/`) has been updated reflecting new architectures.
- [ ] `CHANGELOG.md` is populated with `Added`, `Changed`, `Fixed`, and `Removed` entries.
- [ ] `python -m build` successfully generates valid `.whl` and `.tar.gz` distributions.
- [ ] Docker image (`docker build -t reconx:latest .`) successfully builds.
- [ ] Pre-release smoke test passes (`reconx workflow run test`).
- [ ] Create GitHub Release with compiled release notes.
