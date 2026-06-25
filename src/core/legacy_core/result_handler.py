import os

from core.legacy_core.job_db import Job, JobLog, SessionLocal


class ResultHandler:
    @staticmethod
    def save_results(job_id):
        db = SessionLocal()
        job = db.query(Job).filter(Job.id == job_id).first()
        if not job or not job.project_id:
            db.close()
            return

        proj_dir = os.path.join("projects", job.project_id, "scans")
        if not os.path.exists(proj_dir):
            os.makedirs(proj_dir, exist_ok=True)

        logs = db.query(JobLog).filter(JobLog.job_id == job_id).order_by(JobLog.timestamp).all()

        stdout_path = os.path.join(proj_dir, f"{job.tool_id}_{job_id}_stdout.log")
        stderr_path = os.path.join(proj_dir, f"{job.tool_id}_{job_id}_stderr.log")

        with open(stdout_path, "w") as f_out, open(stderr_path, "w") as f_err:
            for log in logs:
                if log.output_type == "stdout":
                    f_out.write(log.content + "\n")
                else:
                    f_err.write(log.content + "\n")

        db.close()
