from reconx.workflow.models.workflow import Workflow, WorkflowTask


def get_cloud_tools(target_type: str) -> list[dict]:
    if target_type == "aws":
        return [{"id": "scoutsuite", "plugin": "scoutsuite", "depends_on": []}]
    elif target_type == "kubernetes":
        return [{"id": "kubectl", "plugin": "kubectl", "depends_on": []}]
    elif target_type == "container":
        return [
            {"id": "trivy", "plugin": "trivy", "depends_on": []},
            {"id": "dockerbench", "plugin": "dockerbench", "depends_on": []},
        ]
    return []


class CloudWorkflowBuilder:
    @staticmethod
    def build(target: str, target_type: str) -> Workflow:
        tasks_config = get_cloud_tools(target_type)
        tasks = []
        for tc in tasks_config:
            tasks.append(
                WorkflowTask(
                    id=tc["id"],
                    plugin=tc["plugin"],
                    depends_on=tc.get("depends_on", []),
                    args=tc.get("args", {}),
                )
            )

        workflow_id = f"cloud_{target_type}_{target.replace(':', '_').replace('/', '_')}"
        return Workflow(id=workflow_id, name=f"Cloud/Container ({target_type})", tasks=tasks)
