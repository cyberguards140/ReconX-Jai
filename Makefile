.PHONY: install test up down lint help

install:
	@echo "Installing ReconX Python Backend Dependencies..."
	pip install -e .
	pip install -r requirements.txt || true

test:
	@echo "Executing Pytest Mock Suite (AI Swarm Validation)..."
	pytest tests/

up:
	@echo "Booting the ReconX X Enterprise Cluster..."
	docker-compose -f docker-compose.x.yml up --build -d
	@echo "Cluster Online! Access Swagger at http://localhost:8000/docs"

down:
	@echo "Tearing down the ReconX X Cluster..."
	docker-compose -f docker-compose.x.yml down

lint:
	@echo "Running Static Analysis..."
	python -m compileall -q src/

help:
	@echo "ReconX Developer Commands:"
	@echo "  make install  - Install Python dependencies"
	@echo "  make test     - Run the Pytest suite"
	@echo "  make up       - Boot the Docker Compose stack"
	@echo "  make down     - Tear down the stack"
	@echo "  make lint     - Run static analysis checks"
