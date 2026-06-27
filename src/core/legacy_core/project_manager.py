import json
import os

from core.legacy_core.project_db import HistoryEvent, Project, SessionLocal, Target


class ProjectManager:
    @staticmethod
    def create_project(name, description, client, tags):
        db = SessionLocal()
        existing = db.query(Project).filter(Project.name == name).first()
        if existing:
            db.close()
            return None

        tags_str = json.dumps(tags) if tags else "[]"
        project = Project(name=name, description=description, client=client, tags=tags_str)
        db.add(project)
        db.commit()
        db.refresh(project)

        ProjectManager.scaffold_project_directories(project.name)
        ProjectManager.log_history(
            db, project.id, "Project Created", f"Project {name} initialized."
        )

        db.close()
        return project.id

    @staticmethod
    def scaffold_project_directories(project_name):
        base_dir = os.path.abspath(
            os.path.join(os.path.expanduser("~/ReconX/projects"), project_name)
        )
        dirs = [
            "assets",
            "findings",
            "cloud",
            "reports",
            "scans",
            "screenshots",
            "notes",
            "exports",
            "history",
        ]
        for d in dirs:
            os.makedirs(os.path.join(base_dir, d), exist_ok=True)

    @staticmethod
    def add_target(project_id, target_type, value):
        db = SessionLocal()
        t = Target(project_id=project_id, target_type=target_type, value=value)
        db.add(t)
        ProjectManager.log_history(
            db, project_id, "Target Added", f"Added target {value} ({target_type})."
        )
        db.commit()
        db.close()

    @staticmethod
    def archive_project(project_id):
        db = SessionLocal()
        project = db.query(Project).filter(Project.id == project_id).first()
        if project:
            project.status = "Archived"
            ProjectManager.log_history(
                db, project_id, "Project Archived", f"Project {project.name} archived."
            )
            db.commit()
        db.close()

    @staticmethod
    def log_history(db, project_id, event_type, message):
        ev = HistoryEvent(project_id=project_id, event_type=event_type, message=message)
        db.add(ev)
