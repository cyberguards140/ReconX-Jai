from core.graph_db import SessionLocal, Investigation, InvestigationNote
from dashboard.backend.websocket import broadcast

class InvestigationWorkspace:
    @staticmethod
    def create_investigation(project_id, title):
        db = SessionLocal()
        inv = Investigation(project_id=project_id, title=title)
        db.add(inv)
        db.commit()
        db.refresh(inv)
        i_id = inv.id
        
        broadcast({"type": "investigation_created", "project_id": project_id, "investigation_id": i_id})
        db.close()
        return i_id

    @staticmethod
    def add_note(investigation_id, author, note_text):
        db = SessionLocal()
        note = InvestigationNote(investigation_id=investigation_id, author=author, note=note_text)
        db.add(note)
        db.commit()
        db.close()
        return True
