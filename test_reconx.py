import os
import sys
import pytest

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

MODULES_TO_TEST = [
    ("Stage 2: Tool Registry", ["tool_manager.registry_loader", "tool_manager.category_loader"]),
    ("Stage 3: Argument Engine", ["argument_engine.argument_loader", "argument_engine.schema_validator"]),
    ("Stage 4: UI Engine", []),
    ("Stage 5: Execution Engine", ["execution.engine", "execution.job_tracker", "execution.process_runner"]),
    ("Stage 6: Streaming & Parsers", ["streaming.stream_manager", "streaming.websocket_server", "streaming.parsers.nmap_parser"]),
    ("Stage 7: Results Processing Engine", ["processing.parser_engine", "processing.normalization_engine", "processing.asset_manager"]),
    ("Stage 8: Project Manager", ["project_manager.project_service", "project_manager.workspace_loader"]),
    ("Stage 10: Pipeline Engine", ["pipeline_engine.orchestrator", "pipelines.recon_pipeline"]),
]

@pytest.mark.parametrize("name,imports", MODULES_TO_TEST)
def test_imports(name, imports):
    """Dynamically test imports of all major components."""
    for imp in imports:
        try:
            exec(f"import {imp}")
        except Exception as e:
            pytest.fail(f"Failed to import {imp}: {e}")
