from recon.modules.osint.profiles import OSINTProfile, get_osint_tools
from platform_core.workflow_engine.workflow.models.workflow import Workflow, WorkflowTask


class OSINTWorkflowBuilder:
    @staticmethod
    def build(target: str, profile: OSINTProfile) -> Workflow:
        tasks_config = get_osint_tools(profile)
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

        workflow_id = f"osint_{profile.value}_{target.replace('.', '_')}"
        return Workflow(id=workflow_id, name=f"OSINT Collection ({profile.value})", tasks=tasks)
