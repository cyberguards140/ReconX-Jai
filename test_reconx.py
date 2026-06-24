import os
import sys

print("--- Testing ReconX Architecture 1 by 1 ---")

def test_module(name, imports):
    print(f"\nTesting {name}...")
    try:
        for imp in imports:
            exec(f"import {imp}")
            print(f"  ✓ {imp} imported successfully")
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"  [X] FAILED: {e}")

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

test_module("Stage 2: Tool Registry", ["tool_manager.registry_loader", "tool_manager.category_loader"])
test_module("Stage 3: Argument Engine", ["argument_engine.argument_loader", "argument_engine.schema_validator"])
test_module("Stage 4: UI Engine (Frontend check)", [])
test_module("Stage 5: Execution Engine", ["execution.engine", "execution.job_tracker", "execution.process_runner"])
test_module("Stage 6: Streaming & Parsers", ["streaming.stream_manager", "streaming.websocket_server", "streaming.parsers.nmap_parser"])
test_module("Stage 7: Results Processing Engine", ["processing.parser_engine", "processing.normalization_engine", "processing.asset_manager"])
test_module("Stage 8: Project Manager", ["project_manager.project_service", "project_manager.workspace_loader"])
test_module("Stage 9: Dashboard Metrics", ["dashboard_data.metrics_engine", "dashboard_data.chart_engine"])
test_module("Stage 10: Pipeline Engine", ["pipeline_engine.orchestrator", "pipelines.recon_pipeline"])

print("\n--- Syntax & Import Checks Completed ---")
