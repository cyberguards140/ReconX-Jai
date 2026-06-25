from core.legacy_core.process_manager import ProcessManager
from core.legacy_core.queue_manager import QueueManager


class ExecutionEngine:
    @staticmethod
    def queue_job(tool_id, project_id, target, command):
        return QueueManager.add_job(tool_id, project_id, target, command)

    @staticmethod
    def stop_job(job_id):
        return ProcessManager.stop_process(job_id)
