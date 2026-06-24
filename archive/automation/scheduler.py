from core.automation_db import SessionLocal, ScheduledJob

class SchedulerEngine:
    @staticmethod
    def schedule_job(workflow_id, frequency, time):
        db = SessionLocal()
        job = ScheduledJob(workflow_id=workflow_id, frequency=frequency, time=time)
        db.add(job)
        db.commit()
        db.refresh(job)
        job_id = job.id
        db.close()
        return job_id

    @staticmethod
    def list_schedules():
        db = SessionLocal()
        jobs = db.query(ScheduledJob).all()
        res = [{"id": j.id, "workflow": j.workflow_id, "freq": j.frequency, "time": j.time} for j in jobs]
        db.close()
        return res
