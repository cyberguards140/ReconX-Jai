import pytest
from reconx.workflow.validator import WorkflowValidator
from reconx.workflow.exceptions import WorkflowValidationError

def test_invalid_missing_fields():
    validator = WorkflowValidator()
    with pytest.raises(WorkflowValidationError):
        validator.validate_workflow_def({})

def test_invalid_duplicate_ids():
    validator = WorkflowValidator()
    with pytest.raises(WorkflowValidationError):
        validator.validate_workflow_def({
            "name": "test",
            "tasks": [
                {"id": "A", "plugin": "test"},
                {"id": "A", "plugin": "test2"}
            ]
        })

def test_invalid_missing_dependency():
    validator = WorkflowValidator()
    with pytest.raises(WorkflowValidationError):
        validator.validate_workflow_def({
            "name": "test",
            "tasks": [
                {"id": "A", "plugin": "test", "depends_on": ["B"]}
            ]
        })

def test_valid_workflow():
    validator = WorkflowValidator()
    validator.validate_workflow_def({
        "name": "test",
        "tasks": [
            {"id": "A", "plugin": "test"},
            {"id": "B", "plugin": "test", "depends_on": ["A"]}
        ]
    })
    # Should not raise
