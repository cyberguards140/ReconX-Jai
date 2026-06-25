# ReconX v4.0

ReconX is an autonomous, declarative Offensive Security Reconnaissance Framework.

## Features
- **Declarative YAML Workflows:** Chain plugins as a Directed Acyclic Graph.
- **Async Execution:** Heavy parallelization using asyncio and thread pools.
- **Plugin Architecture:** Write tools in bash or python and wrap them natively.
- **REST API:** Control execution dynamically via FastAPI.
- **Advanced Agent AI:** Built-in meta-learning and predictive modeling.

## Prerequisites
- Python 3.11 or higher
- Git

## Setup and Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/reconx/reconx.git
   cd reconx/product
   ```

2. **Set up a Virtual Environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

3. **Install the Application:**
   ```bash
   pip install -e .
   ```

4. **Environment Variables:**
   Copy the example environment file and update it with your settings.
   ```bash
   cp .env.example .env
   ```
   **Key `.env` variables:**
   - `DATABASE_URL`: Connection string for the database (e.g., `sqlite+aiosqlite:///reconx.db`)
   - `LOG_LEVEL`: Logging verbosity (default: `INFO`)
   - `PLUGIN_TIMEOUT` / `WORKFLOW_TIMEOUT`: Execution limits
   - `JWT_SECRET`: Secret used for API authentication

## Configuration

ReconX uses a `config.yaml` file for core framework settings. You can find or create it in the project root.
Key configuration sections include:

- **meta_learning**: Enable self-optimization and learning cycles.
- **saas / distributed**: Set up multi-tenancy, multi-region support, and background workers.
- **agent**: Configure autonomy levels, goal-based execution, and memory persistence.
- **stealth**: Settings for passive mode and jitter range.
- **plugins_enabled**: A list of plugins active by default (e.g., `dns_enum`, `port_scan`).

## Usage

ReconX provides a CLI for managing workflows, assets, and reports. 
Run `reconx --help` to see all available commands.

**Examples:**
```bash
# Check the version
reconx version

# View the dashboard
reconx dashboard

# List all findings
reconx findings

# Manage workflows
reconx workflow --help
```
