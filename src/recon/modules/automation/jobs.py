class JobDefinition:
    def __init__(self, job_type: str):
        self.job_type = job_type

    def to_dict(self):
        return {"job_type": self.job_type, "status": "Pending"}
