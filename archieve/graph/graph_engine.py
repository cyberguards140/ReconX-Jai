from core.graph_db import SessionLocal, GraphEntity, GraphRelationship
from dashboard.backend.websocket import broadcast

class GraphEngine:
    @staticmethod
    def add_entity(project_id, entity_type, entity_value):
        db = SessionLocal()
        e = db.query(GraphEntity).filter_by(project_id=project_id, entity_type=entity_type, entity_value=entity_value).first()
        if not e:
            e = GraphEntity(project_id=project_id, entity_type=entity_type, entity_value=entity_value)
            db.add(e)
            db.commit()
            db.refresh(e)
            broadcast({"type": "entity_created", "project_id": project_id, "entity_id": e.id})
        res = e.id
        db.close()
        return res

    @staticmethod
    def add_relationship(project_id, source_id, target_id, relation_type, confidence=100.0):
        db = SessionLocal()
        r = db.query(GraphRelationship).filter_by(source_id=source_id, target_id=target_id, relation_type=relation_type).first()
        if not r:
            r = GraphRelationship(project_id=project_id, source_id=source_id, target_id=target_id, relation_type=relation_type, confidence_score=confidence)
            db.add(r)
            db.commit()
            broadcast({"type": "relationship_added", "project_id": project_id, "relation_type": relation_type})
        db.close()
        return True
