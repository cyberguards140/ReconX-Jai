# Docker Validation

## .dockerignore
```
archive/
workspace/
tests/
docs/
.git/
.github/
*.env
*.log

```
## Dockerfile
```dockerfile
FROM python:3.11-slim

RUN groupadd -r reconx && useradd -r -g reconx reconx

WORKDIR /app
COPY pyproject.toml .
COPY src/ ./src/

RUN pip install .

USER reconx

HEALTHCHECK --interval=30s --timeout=3s \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

EXPOSE 8000
CMD ["python", "-m", "reconx.cli.main", "api", "--port", "8000"]

```
