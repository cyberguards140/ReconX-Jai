from platform_core.workflow_engine.workflow.models.workflow import Workflow, WorkflowTask
from recon.modules.content_discovery.profiles import ContentProfile, get_content_tools


class ContentWorkflowBuilder:
    @staticmethod
    def build(target: str, profile: ContentProfile) -> Workflow:
        tasks_config = get_content_tools(profile)
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

        workflow_id = f"content_{profile.value}_{target.replace('://', '_').replace('.', '_').replace('/', '')}"
        return Workflow(id=workflow_id, name=f"Content Discovery ({profile.value})", tasks=tasks)
