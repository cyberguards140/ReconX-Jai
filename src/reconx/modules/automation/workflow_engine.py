class AutomationWorkflowCore:
    @staticmethod
    def get_workflow_tasks(workflow_name: str) -> list[str]:
        workflows = {
            "QuickRecon": ["DNS", "Subdomains", "Technologies"],
            "Standard": ["QuickRecon", "WebAssessment"],
        }
        return workflows.get(workflow_name, [])
