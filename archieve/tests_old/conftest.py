import pytest

@pytest.fixture
def sample_project():
    return {
        "project_id": "test_project"
    }

@pytest.fixture
def sample_plugin_output():
    return {
        "status": "success",
        "data": {"open_ports": [80, 443]}
    }
