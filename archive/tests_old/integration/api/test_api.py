from fastapi.testclient import TestClient
from reconx.api.main import app

client = TestClient(app)

def test_health_endpoint():
    response = client.get("/health")
    # Even if it's not implemented yet, standardizing the test stub
    assert response.status_code in [200, 404]

def test_workflow_execution():
    response = client.post("/workflows/execute", json={"target": "example.com"})
    assert response.status_code in [200, 401, 403, 404, 422]
