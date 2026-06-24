class WorkflowManager:
    """
    Handles task assignments, approval flows, and response tracking for analysts.
    """
    def __init__(self):
        self.tasks = []

    def assign_task(self, case_id: str, task_name: str, assignee: str):
        self.tasks.append({
            "case_id": case_id,
            "task_name": task_name,
            "assignee": assignee,
            "status": "Pending"
        })
