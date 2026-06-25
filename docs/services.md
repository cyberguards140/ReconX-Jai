# Services Layer

The Service Layer establishes an explicit boundary between presentation layers (API / CLI) and infrastructural engines (Workflow Engine, Plugin Manager, Database).

## Architecture Flow

```
[ FastAPI Routes ]  [ Typer CLI Commands ]
         │                  │
         └───────┐  ┌───────┘
                 ▼  ▼
      [ Service Layer (e.g. WorkflowService) ]
                 │
      ┌──────────┼──────────┐
      ▼          ▼          ▼
[ Workflow ] [ Plugin ] [ Database ]
[ Engine   ] [ Manager] [ Session  ]
```

## Rules

1. **No direct DB queries from routes**: The API layer requests an action through the Service, which then initiates `async_session_factory()`.
2. **Abstracted State**: Components like `StateManager` are strictly called within the Service layer methods (e.g. `cancel_workflow`).
3. **Singleton Support**: CLI modules use instantiated singletons (`workflow_service`), whereas API routes rely on `Depends(get_workflow_service)`.
