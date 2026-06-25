from core.legacy_core.job_db import SessionLocal, Job, JobLog
from datetime import datetime

class JobManager:
    @staticmethod
    def create_job(tool_id, project_id, target, command):
        db = SessionLocal()
        job = Job(
            tool_id=tool_id,
            project_id=project_id,
            target=target,
            command=command,
            status="queued"
        )
        db.add(job)
        db.commit()
        db.refresh(job)
        job_id = job.id
        db.close()
        return job_id

    @staticmethod
    def update_status(job_id, status, pid=None):
        db = SessionLocal()
        job = db.query(Job).filter(Job.id == job_id).first()
        if job:
            job.status = status
            if pid:
                job.pid = pid
            if status == "running" and not job.started:
                job.started = datetime.utcnow()
            elif status in ["completed", "failed", "cancelled"]:
                job.finished = datetime.utcnow()
            db.commit()
        db.close()

    @staticmethod
    def log_output(job_id, output_type, content):
        db = SessionLocal()
        db.add(JobLog(job_id=job_id, output_type=output_type, content=content))
        db.commit()
        db.close()

    @staticmethod
    def get_job(job_id):
        db = SessionLocal()
        job = db.query(Job).filter(Job.id == job_id).first()
        if job:
            res = {
                "id": job.id, "tool_id": job.tool_id, "project_id": job.project_id,
                "target": job.target, "command": job.command, "status": job.status,
                "pid": job.pid, "started": job.started.isoformat() if job.started else None,
                "finished": job.finished.isoformat() if job.finished else None
            }
        else:
            res = None
        db.close()
        return res

    @staticmethod
    def get_jobs_by_status(status):
        db = SessionLocal()
        jobs = db.query(Job).filter(Job.status == status).all()
        res = [{"id": j.id, "tool_id": j.tool_id, "target": j.target} for j in jobs]
        db.close()
        return res
