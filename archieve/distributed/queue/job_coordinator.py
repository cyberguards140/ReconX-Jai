from core.distributed_db import SessionLocal, DistributedJob, JobAssignment, Node
from dashboard.backend.websocket import broadcast

class JobCoordinator:
    @staticmethod
    def queue_job(job_name, payload_json):
        db = SessionLocal()
        job = DistributedJob(job_name=job_name, payload=payload_json, status="Queued")
        db.add(job)
        db.commit()
        db.refresh(job)
        job_id = job.id
        db.close()
        return job_id

    @staticmethod
    def assign_jobs():
        db = SessionLocal()
        queued_jobs = db.query(DistributedJob).filter(DistributedJob.status == "Queued").all()
        available_nodes = db.query(Node).filter(Node.status == "Online").all()
        
        if not available_nodes:
            db.close()
            return
            
        for idx, job in enumerate(queued_jobs):
            node = available_nodes[idx % len(available_nodes)]
            job.status = "Assigned"
            
            assignment = JobAssignment(job_id=job.id, node_id=node.id)
            db.add(assignment)
            
            broadcast({
                "type": "job_assigned",
                "job_name": job.job_name,
                "node_hostname": node.hostname
            })
            
        db.commit()
        db.close()
