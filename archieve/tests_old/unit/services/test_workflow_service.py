import pytest
from unittest.mock import patch, AsyncMock
from reconx.services.workflow_service import WorkflowService

@pytest.mark.asyncio
@patch('reconx.services.workflow_service.workflow_engine.execute_workflow', new_callable=AsyncMock)
async def test_start_workflow(mock_execute):
    mock_execute.return_value = {"status": "SUCCESS", "execution_id": "test-id"}
    
    service = WorkflowService()
    result = await service.start_workflow("test-wf", "localhost", "user-1")
    
    assert result["status"] == "SUCCESS"
    assert result["execution_id"] == "test-id"
    mock_execute.assert_called_once_with("test-wf", "localhost", "user-1")

@pytest.mark.asyncio
async def test_list_workflows():
    service = WorkflowService()
    # It reads from disk, so we can mock glob or just test it runs
    with patch('glob.glob', return_value=['src/reconx/workflows/test.yaml']):
        workflows = await service.list_workflows()
        assert "test" in workflows
