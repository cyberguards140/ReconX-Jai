# ReconX Architecture Documentation

## Components

### CLI
Typer-based user entrypoints located in `src/reconx/cli/`. Handles immediate user interaction, dispatching commands to the Workflow Engine or direct services.

### API
FastAPI backend located in `src/reconx/api/`. Responsible for RESTful routing, schema validation, and serving remote clients. No heavy logic resides here; it acts purely as a transport layer delegating to services.

### Workflow Engine
Located in `src/reconx/workflow/`. Acts as the central nervous system. Parses DAG logic, handles scheduling, dependency resolution, orchestrates tasks, and catches top-level isolations.

### Plugin Layer
Located in `src/reconx/plugins/`. Contains the `PluginManager`, `PluginRegistry`, and tool `adapters`. This layer safely executes bash/python wrappers using asynchronous subprocesses and standardizes tool STDOUT to JSON lines.

### Database Layer
Located in `src/reconx/database/`. Houses SQLAlchemy models, repositories, database connection sessions, and schema migrations. Strictly independent; it provides data persistence to services but never imports from the API or CLI layer.

### Services
Located in `src/reconx/services/`. Business logic domains such as Intelligence handling, Reporting, and Authentication logic. Connects Workflow outputs with the Database.

### Events
Located in `src/reconx/events/`. Central `event_bus` managing asynchronous state transitions across decoupled domains.

---

## Data Flow Pipeline

```text
User
 ↓
CLI / API
 ↓
Workflow Engine
 ↓
Plugin Manager
 ↓
Tool Adapter
 ↓
Parser (JSON Lines)
 ↓
Services (Result Aggregation / Normalization)
 ↓
Database (Intelligence Store)
```
