from reconx.workflow.models.workflow import Workflow, WorkflowTask
from reconx.modules.smb.profiles import get_smb_tools, SMBProfile

class SMBWorkflowBuilder:
    @staticmethod
    def build(target: str, profile: SMBProfile) -> Workflow:
        tasks_config = get_smb_tools(profile)
        tasks = []
        for tc in tasks_config:
            tasks.append(WorkflowTask(
                id=tc["id"],
                plugin=tc["plugin"],
                depends_on=tc.get("depends_on", []),
                args=tc.get("args", {})
            ))
            
        workflow_id = f"smb_{profile.value}_{target.replace('.', '_')}"
        return Workflow(id=workflow_id, name=f"SMB Enumeration ({profile.value})", tasks=tasks)
