from distributed.queue.job_coordinator import JobCoordinator

class ControllerOrchestrator:
    @staticmethod
    def receive_workflow_task(task_name, payload):
        """
        Receives tasks from the Stage 15 automation scheduler and bridges them to the distributed nodes.
        """
        print(f"[Orchestrator] Orchestrating workflow task: {task_name}")
        JobCoordinator.queue_job(task_name, payload)
        # Attempt immediate distribution if nodes are free
        JobCoordinator.assign_jobs()
