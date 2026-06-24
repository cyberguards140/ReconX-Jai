class JobQueueService:
    def __init__(self):
        self.queue = []
        
    def enqueue(self, job: dict):
        job["status"] = "Pending"
        self.queue.append(job)
        
    def execute_next(self):
        if self.queue:
            job = self.queue.pop(0)
            job["status"] = "Completed"
            return job
        return None
