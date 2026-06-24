# ReconX API Reference

The ReconX API provides a uniform HTTP gateway into the core services layer. It adheres to strict Pydantic schemas and standard response mappings.

## Standard Responses

All API endpoints return the `StandardResponse` model:
```json
{
  "success": true,
  "data": { ... }
}
```

Failed endpoints strictly return error details and an appropriate HTTP status code mapping:
```json
{
  "success": false,
  "error": {
    "code": "WORKFLOW_NOT_FOUND",
    "message": "The workflow requested does not exist."
  }
}
```

## Global Exception Handling

Custom logic exceptions like `WorkflowNotFoundError` or `PluginExecutionError` inherit from `ReconXException`. The API layer globally traps these exceptions and transforms them into standardized `404` or `500` JSON payloads.

## Dependency Injection

All business operations rely on injected services (`Depends(get_workflow_service)`). The API routes themselves never instantiate logic engines, orchestrators, or the Database Session directly. This allows isolated unit testing via FastAPI overrides.

## Middleware

- `RequestLoggingMiddleware`: Access logs.
- `CorrelationMiddleware`: Assigns and returns a unique `X-Correlation-ID` header.
- `ResponseTimingMiddleware`: Emits a `X-Process-Time` duration header.