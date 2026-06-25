# ReconX Plugin Ecosystem

The Plugin Ecosystem is the core component that enables ReconX to integrate external reconnaissance tools effortlessly.

## Architecture

The plugin ecosystem strictly separates concerns to guarantee safe execution, rapid discovery, and uniform output schemas.

```text
Plugin
  ↓
Adapter (Implements BaseAdapter, parses STDOUT/JSON)
  ↓
PluginRegistry (Discovers, Validates, and Registers plugins dynamically)
  ↓
PluginManager (Executes plugins inside the sandbox, captures metrics)
  ↓
Intelligence Store
```

### Schemas

All Plugins must inherit from `BasePlugin` and return a `PluginResult` schema.
The schema enforces consistency:

```python
class PluginResult(BaseModel):
    plugin: str
    success: bool
    execution_time: float
    output: Dict[str, Any]
    errors: List[str]
    assets: List[Dict[str, Any]]
    findings: List[Dict[str, Any]]
```

## Development Guide

ReconX includes a Software Development Kit (SDK) via the Typer CLI to instantly generate boilerplate code.

### 1. Scaffold a New Plugin

```bash
python -m reconx.cli.main plugins create my_tool
```

This generates:
- `src/reconx/plugins/adapters/my_tool/plugin.py`
- `src/reconx/plugins/adapters/my_tool/metadata.yaml`
- `src/reconx/plugins/adapters/my_tool/tests/`

### 2. Implement Execution and Parsing

In `plugin.py`, implement the abstract methods from `BaseAdapter`:

- `execute(self, target, context)`: Launch the external tool asynchronously.
- `parse(self, output)`: Read the unstructured output and extract lists of Assets and Findings.

### 3. Automatic Discovery

ReconX automatically parses `src/reconx/plugins/adapters/` at startup. If your plugin module defines `ToolAdapter = MyPluginClass`, it will be registered automatically.
No manual dictionary mapping is required!

### 4. Test the Plugin

```bash
pytest src/reconx/plugins/adapters/my_tool/tests/
```
Ensure your tests pass locally before submitting.