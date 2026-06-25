from core.automation_db import SessionLocal, Workflow, WorkflowStep

class WorkflowEngine:
    DEFAULT_WORKFLOWS = {
        "Quick Recon": ["subfinder", "dnsx", "httpx"],
        "Deep Recon": ["subfinder", "amass", "dnsx", "httpx", "naabu", "nmap"],
        "Vulnerability Assessment": ["nuclei", "nikto", "sslscan"],
        "Web Enumeration": ["katana", "ffuf", "linkfinder", "secretfinder"],
        "Cloud Discovery": ["cloud_discovery", "storage_discovery", "iam_discovery"],
        "Full Assessment": ["subfinder", "dnsx", "httpx", "katana", "nuclei", "cloud_discovery"]
    }

    @staticmethod
    def create_workflow(project_id, name, steps):
        db = SessionLocal()
        wf = Workflow(project_id=project_id, name=name)
        db.add(wf)
        db.commit()
        db.refresh(wf)
        
        for idx, tool in enumerate(steps):
            step = WorkflowStep(workflow_id=wf.id, tool=tool, execution_order=idx+1)
            db.add(step)
            
        db.commit()
        db.close()
        return wf.id

    @staticmethod
    def get_workflows(project_id):
        db = SessionLocal()
        wfs = db.query(Workflow).filter(Workflow.project_id == project_id).all()
        result = []
        for w in wfs:
            steps = db.query(WorkflowStep).filter(WorkflowStep.workflow_id == w.id).order_by(WorkflowStep.execution_order).all()
            result.append({
                "id": w.id,
                "name": w.name,
                "steps": [s.tool for s in steps]
            })
        db.close()
        return result
