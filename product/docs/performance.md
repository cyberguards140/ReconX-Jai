# ReconX Performance Baseline

The following baseline metrics were captured locally using `scripts/workflow_benchmark.py` and `scripts/event_benchmark.py` during the v4.0 stabilization phase.

## Workflow Engine
Resolving, validating, and executing complex DAG matrices (assuming mocked non-blocking async tasks):
- **10 workflows (100 tasks)**: ~0.15s
- **100 workflows (1,000 tasks)**: ~0.8s
- **1000 workflows (10,000 tasks)**: ~3.2s

## Event Bus & Observability
Async event dispatching via `src/reconx/events/bus.py` across 3 active handlers (Logging, Metrics, Persistence):
- **Throughput**: >200,000 events/second
- **Memory Overhead**: ~45MB sustained during high burst windows.

## Plugin Execution
Standalone isolated plugin execution overhead:
- **100 concurrent plugins**: ~0.4s
- **1,000 concurrent plugins**: ~1.1s
- **10,000 concurrent plugins**: ~4.5s

*Hardware Profile: 8-Core CPU, 16GB RAM, NVMe SSD.*
