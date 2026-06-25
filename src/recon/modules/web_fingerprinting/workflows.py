from platform_core.workflow_engine.workflow.models.workflow import Workflow, WorkflowTask
from recon.modules.web_fingerprinting.profiles import WebProfile, get_web_tools


class WebWorkflowBuilder:
    @staticmethod
    def build(target: str, profile: WebProfile) -> Workflow:
        tasks_config = get_web_tools(profile)
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

        workflow_id = (
            f"web_{profile.value}_{target.replace('://', '_').replace('.', '_').replace('/', '')}"
        )
        return Workflow(id=workflow_id, name=f"Web Fingerprinting ({profile.value})", tasks=tasks)
