# ADR Gap Analysis

## ADR-001 (Plugin System)
Expected: Single plugin system
Reality: Multiple plugin systems detected (e.g. `plugins/` vs `core/plugin_manager/`)
Gap: Delete secondary system and unify under `core/plugin_manager/`.

## ADR-002 (Workflow Engine)
Expected: Centralized workflow execution
Reality: Workflows scattered or missing
Gap: Implement core/workflow_engine.py.

## ADR-003 (Event Bus)
Expected: Event-driven architecture
Reality: Missing event bus implementation
Gap: Implement core/event_bus.py.

## ADR-004 (Scheduler)
Expected: Unified scheduling system
Reality: Missing scheduler implementation
Gap: Implement core/scheduler.py.
