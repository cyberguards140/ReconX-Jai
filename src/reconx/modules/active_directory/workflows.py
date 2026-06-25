from reconx.modules.active_directory.profiles import ADProfile, get_ad_tools
from reconx.workflow.models.workflow import Workflow, WorkflowTask


class ADWorkflowBuilder:
    @staticmethod
    def build(target: str, profile: ADProfile) -> Workflow:
        tasks_config = get_ad_tools(profile)
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

        workflow_id = f"ad_{profile.value}_{target.replace('.', '_')}"
        return Workflow(id=workflow_id, name=f"AD Enumeration ({profile.value})", tasks=tasks)
