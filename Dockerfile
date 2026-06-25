# Stage 1: Build dependencies
FROM python:3.13-slim as builder

WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install system dependencies needed for compilation
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
# Install into a temporary prefix
RUN pip install --user --no-cache-dir -r requirements.txt

# Install optional high-performance and distributed platform dependencies
# We ensure celery, redis, aiokafka, and confluent-kafka are available
RUN pip install --user --no-cache-dir redis aiokafka confluent-kafka celery

# Stage 2: Production runtime
FROM python:3.13-slim

WORKDIR /app
ENV PYTHONPATH=/app/src
ENV PATH="/root/.local/bin:${PATH}"

# Install runtime system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy python packages from builder
COPY --from=builder /root/.local /root/.local

# Copy application source
COPY src/ /app/src/

# Create a non-root user for security
RUN adduser --disabled-password --gecos '' reconx
RUN chown -R reconx:reconx /app
USER reconx

# Default command for API Gateway / Web layer
CMD ["uvicorn", "reconx.api.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
