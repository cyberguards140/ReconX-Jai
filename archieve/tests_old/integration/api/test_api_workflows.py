from fastapi.testclient import TestClient
from reconx.api.main import app
from reconx.api.dependencies import get_current_user
from reconx.database.models import User

client = TestClient(app)

def override_get_current_user():
    user = User()
    user.id = "test-user"
    user.role = "admin"
    return user

app.dependency_overrides[get_current_user] = override_get_current_user

def test_list_workflows():
    response = client.get("/api/v1/workflows")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert isinstance(data["data"], list)

def test_workflow_not_found():
    response = client.get("/api/v1/workflows/executions/invalid_id")
    assert response.status_code == 404
    data = response.json()
    assert data["success"] is False
    assert data["error"]["code"] == "WORKFLOW_NOT_FOUND"
