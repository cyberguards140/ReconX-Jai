# Workflow Engine

The ReconX Workflow Engine orchestrates Directed Acyclic Graphs (DAGs) of tasks asynchronously.

## Workflow Lifecycle

1. **Create/Load**: Workflows are loaded from YAML definitions.
2. **Validate**: The `WorkflowValidator` ensures there are no duplicate IDs, no missing dependencies, and structural compliance.
3. **Graph Construction**: The `DependencyGraph` builds the DAG and runs cycle detection. Topologies containing cycles are strictly rejected.
4. **Execution/Scheduling**: `WorkflowScheduler` queues topological layers of the graph, pushing available tasks into the `TaskExecutor`.
5. **Persistence**: `StateManager` tracks state changes natively back to the SQL database using `WorkflowState` Enums.
6. **Completion/Failure**: The workflow halts gracefully upon completion, handles skipping dependent tasks if a parent fails, and propagates the final `PluginResult` outputs into the `IntelligenceStore`.

## DAG Concepts

- **Nodes**: Represent individual `WorkflowTask` executions targeting a plugin.
- **Edges**: The `depends_on` array forms directed edges.
- **Cycle Detection**: Kahn's topological sort ensures loops (A -> B -> C -> A) are blocked before runtime.

## State Machine

The system strictly adheres to the following transition definitions:

- **Workflow States (`WorkflowState`)**: `PENDING`, `RUNNING`, `COMPLETED`, `FAILED`, `CANCELLED`
- **Task States (`TaskStatus`)**: `PENDING`, `RUNNING`, `SUCCESS`, `FAILED`, `SKIPPED`, `CANCELLED`

### Retries & Skipping
If a `Task` fails its execution limits (`retries`), it is marked `FAILED`. Any downstream tasks that declare this failed task in `depends_on` are automatically marked as `SKIPPED`.

### Cancellation
Users can dispatch a cancellation request by Execution ID. The `WorkflowScheduler` traps this flag, issues `asyncio.CancelledError` signals to the active routines, and transitions incomplete tasks to `CANCELLED`.
