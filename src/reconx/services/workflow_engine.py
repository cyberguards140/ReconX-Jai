from reconx.modules.automation.workflow_engine import AutomationWorkflowCore

class WorkflowEngineService:
    @staticmethod
    def build_workflow(name: str) -> list[str]:
        return AutomationWorkflowCore.get_workflow_tasks(name)
