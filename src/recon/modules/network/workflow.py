from platform_core.workflow_engine.workflow.models.workflow import Workflow, WorkflowTask
from recon.modules.network.profiles import ScanProfile, get_profile_tools


class NetworkWorkflowBuilder:
    """Dynamically builds a ReconX Workflow object based on a network profile."""

    @staticmethod
    def build(target: str, profile: ScanProfile) -> Workflow:
        tasks_config = get_profile_tools(profile)
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

        workflow_id = f"network_{profile.value}_{target.replace('.', '_')}"
        return Workflow(id=workflow_id, name=f"Network Recon ({profile.value})", tasks=tasks)
