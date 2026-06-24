from typer.testing import CliRunner
from reconx.cli.main import app
from unittest.mock import patch, AsyncMock

runner = CliRunner()

@patch('reconx.cli.workflow.workflow_service.list_workflows', new_callable=AsyncMock)
def test_cli_list_workflows(mock_list):
    mock_list.return_value = ["test-workflow"]
    
    result = runner.invoke(app, ["workflow", "list"])
    assert result.exit_code == 0
    assert "Available Workflows" in result.stdout
    assert "test-workflow" in result.stdout

@patch('reconx.cli.workflow.workflow_service.start_workflow', new_callable=AsyncMock)
def test_cli_run_workflow(mock_start):
    mock_start.return_value = {"status": "SUCCESS", "execution_id": "123"}
    
    result = runner.invoke(app, ["workflow", "run", "test-workflow", "127.0.0.1"])
    assert result.exit_code == 0
    assert "Workflow completed successfully" in result.stdout
    assert "123" in result.stdout
