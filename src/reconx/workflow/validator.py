from typing import Dict, Any
from reconx.workflow.exceptions import WorkflowValidationError

class WorkflowValidator:
    def validate_workflow_def(self, data: Dict[str, Any]) -> None:
        if "name" not in data or not data["name"]:
            raise WorkflowValidationError("Workflow must have a valid 'name'")
        if "tasks" not in data or not isinstance(data["tasks"], list) or not data["tasks"]:
            raise WorkflowValidationError("Workflow must contain a non-empty 'tasks' list")

        task_ids = set()
        for task in data["tasks"]:
            if "id" not in task or not task["id"]:
                raise WorkflowValidationError("Every task must have an 'id'")
            if task["id"] in task_ids:
                raise WorkflowValidationError(f"Duplicate task id detected: {task['id']}")
            task_ids.add(task["id"])

        for task in data["tasks"]:
            deps = task.get("depends_on", [])
            for dep in deps:
                if dep not in task_ids:
                    raise WorkflowValidationError(f"Task '{task['id']}' depends on unknown task '{dep}'")
