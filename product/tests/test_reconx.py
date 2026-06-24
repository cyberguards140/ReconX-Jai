import os
import sys
import pytest

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

MODULES_TO_TEST = [
    ("Stage 2: Tool Registry", ["reconx.tool_manager.registry_loader", "reconx.tool_manager.category_loader"]),
    ("Stage 3: Argument Engine", ["reconx.argument_engine.argument_loader", "reconx.argument_engine.schema_validator"]),
    ("Stage 4: UI Engine", []),
    ("Stage 5: Execution Engine", ["reconx.execution.engine", "reconx.execution.job_tracker", "reconx.execution.process_runner"]),
    ("Stage 6: Streaming & Parsers", ["reconx.streaming.stream_manager", "reconx.streaming.websocket_server", "reconx.streaming.parsers.nmap_parser"]),
    ("Stage 7: Results Processing Engine", ["reconx.processing.parser_engine", "reconx.processing.normalization_engine", "reconx.processing.asset_manager"]),
    ("Stage 8: Project Manager", ["reconx.project_manager.project_service", "reconx.project_manager.workspace_loader"]),
    ("Stage 10: Pipeline Engine", ["reconx.pipeline_engine.orchestrator", "reconx.pipelines.recon_pipeline"]),
]

@pytest.mark.parametrize("name,imports", MODULES_TO_TEST)
def test_imports(name, imports):
    """Dynamically test imports of all major components."""
    for imp in imports:
        try:
            exec(f"import {imp}")
        except Exception as e:
            pytest.fail(f"Failed to import {imp}: {e}")
