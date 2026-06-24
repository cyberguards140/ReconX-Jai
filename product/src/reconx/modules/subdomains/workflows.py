from reconx.workflow.models.workflow import Workflow, WorkflowTask
from reconx.modules.subdomains.profiles import get_subdomain_tools, SubdomainProfile

class SubdomainWorkflowBuilder:
    @staticmethod
    def build(domain: str, profile: SubdomainProfile) -> Workflow:
        tasks_config = get_subdomain_tools(profile)
        tasks = []
        for tc in tasks_config:
            tasks.append(WorkflowTask(
                id=tc["id"],
                plugin=tc["plugin"],
                depends_on=tc.get("depends_on", []),
                args=tc.get("args", {})
            ))
            
        workflow_id = f"subdom_{profile.value}_{domain.replace('.', '_')}"
        return Workflow(id=workflow_id, name=f"Subdomain Recon ({profile.value})", tasks=tasks)
