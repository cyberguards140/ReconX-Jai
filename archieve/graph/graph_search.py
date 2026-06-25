from core.graph_db import SessionLocal, GraphEntity, GraphRelationship

class GraphSearchEngine:
    @staticmethod
    def search_by_type(project_id, entity_type):
        db = SessionLocal()
        entities = db.query(GraphEntity).filter_by(project_id=project_id, entity_type=entity_type).all()
        res = [{"id": e.id, "value": e.entity_value} for e in entities]
        db.close()
        return res
