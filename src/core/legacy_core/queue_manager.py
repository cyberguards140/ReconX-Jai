from core.legacy_core.job_manager import JobManager

class QueueManager:
    @staticmethod
    def add_job(tool_id, project_id, target, command):
        return JobManager.create_job(tool_id, project_id, target, command)
