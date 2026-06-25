from reconx.modules.dns.profiles import DNSProfile, get_dns_profile_tools
from reconx.workflow.models.workflow import Workflow, WorkflowTask


class DNSWorkflowBuilder:
    @staticmethod
    def build(domain: str, profile: DNSProfile) -> Workflow:
        tasks_config = get_dns_profile_tools(profile)
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

        workflow_id = f"dns_{profile.value}_{domain.replace('.', '_')}"
        return Workflow(id=workflow_id, name=f"DNS Intelligence ({profile.value})", tasks=tasks)
