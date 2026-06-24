from core.queue_manager import QueueManager
from core.process_manager import ProcessManager

class ExecutionEngine:
    @staticmethod
    def queue_job(tool_id, project_id, target, command):
        return QueueManager.add_job(tool_id, project_id, target, command)

    @staticmethod
    def stop_job(job_id):
        return ProcessManager.stop_process(job_id)
