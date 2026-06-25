from platform_core.workflow_engine.workflow.models.workflow import Workflow, WorkflowTask
from recon.modules.subdomains.profiles import SubdomainProfile, get_subdomain_tools


class SubdomainWorkflowBuilder:
    @staticmethod
    def build(domain: str, profile: SubdomainProfile) -> Workflow:
        tasks_config = get_subdomain_tools(profile)
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

        workflow_id = f"subdom_{profile.value}_{domain.replace('.', '_')}"
        return Workflow(id=workflow_id, name=f"Subdomain Recon ({profile.value})", tasks=tasks)
