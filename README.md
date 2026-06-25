# ReconX X (vX.0.0-ULTIMATE)

![ReconX Banner](https://img.shields.io/badge/ReconX-Enterprise_Intelligence-blue?style=for-the-badge&logo=shield)
![Python](https://img.shields.io/badge/Python-3.11+-yellow?style=flat-square&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green?style=flat-square&logo=fastapi)
![Neo4j](https://img.shields.io/badge/Neo4j-Graph_Twin-blue?style=flat-square&logo=neo4j)

**ReconX X** is the world's most advanced Autonomous Attack Surface Management (ASM) and Security Intelligence Platform. Built from the ground up over 100 architectural phases, it mathematically expands from a simple DNS scanner into a distributed, multi-regional, AI-driven digital twin of your enterprise attack surface.

---

## 🌌 Core Architecture

ReconX X is built on a massive, highly scalable distributed architecture:

1. **The Autonomous AI Swarm**: Eliminates manual scanning workflows. A deep-learning daemon automatically discovers seeds, correlates ownership, probes ports, and passes data between the `ReconAgent`, `CorrelationAgent`, and `ReportingAgent`.
2. **The Neo4j Digital Twin**: Maps the entire attack surface as a massive Graph Database. It executes bounded `shortestPath()` Cypher queries to simulate real-world lateral movement and breach paths.
3. **The Global Scale Layer**: Dynamically dispatches workloads via Bitnami Kafka clusters to regional geographic nodes (`us-east`, `eu-central`) to bypass WAFs and geolocation blocks.
4. **The Security Data Fabric**: Automatically translates all internal JSON findings into the standard **OCSF** format for seamless SIEM integration (Splunk, Sentinel).
5. **The Threat Exchange Ecosystem**: A robust SDK and Plugin marketplace that allows independent researchers to upload zero-day signatures and custom nuclei templates.

---

## 🚀 Quickstart

ReconX X is designed to be orchestrated locally using Docker Compose for development and testing.

### Prerequisites
- Docker & Docker Compose
- Python 3.11+ (for local SDK development)
- `make`

### Boot the Monolith
To spin up the entire cluster (API Gateway, PostgreSQL, Neo4j, Redis, Kafka, and the Autonomous Daemons):

```bash
make up
```

Wait 30 seconds for the databases to initialize, then navigate to:
- **Swagger Documentation**: `http://localhost:8000/docs`
- **Neo4j Browser**: `http://localhost:7474` (neo4j/reconx_graph)

---

## 🛠️ Developer Commands

ReconX X includes a `Makefile` to streamline the development lifecycle:

- `make install` : Install the Python backend dependencies.
- `make test` : Execute the Pytest mock suite (securing the AI Swarm).
- `make up` : Boot the Docker Compose stack.
- `make down` : Tear down the cluster and wipe the data.
- `make lint` : Run Python static analysis checks.

---

## 🔒 Enterprise Security

ReconX X is packaged with Enterprise controls suitable for Fortune 500 deployments:
- **SSO**: Generic SAML/OIDC Adapter integration.
- **RBAC**: Strict Role-Based Access Control logic separating `Admin`, `Analyst`, and `Viewer` profiles.
- **Audit Logging**: Append-only, cryptographically secure WORM logging for SOC2/ISO27001 compliance.
- **Rate Limiting**: Native Token Bucket algorithm protecting the API Gateway from volumetric exhaustion attacks.

---

## 📜 License

ReconX X is distributed under an **Enterprise Commercial License**. Please contact `security@reconx.io` for deployment queries and support contracts.
