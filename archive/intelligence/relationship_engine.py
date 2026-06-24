from core.intelligence_db import SessionLocal, Relationship, UniversalAsset
from dashboard.backend.websocket import broadcast

class RelationshipEngine:
    @staticmethod
    def link_assets(source_id, target_id, relation_type):
        db = SessionLocal()
        # Avoid duplicate edges
        existing = db.query(Relationship).filter(
            Relationship.source_id == source_id,
            Relationship.target_id == target_id,
            Relationship.relation_type == relation_type
        ).first()
        
        if existing:
            db.close()
            return existing.id

        rel = Relationship(source_id=source_id, target_id=target_id, relation_type=relation_type)
        db.add(rel)
        db.commit()
        db.refresh(rel)
        
        broadcast({
            "type": "relationship_created",
            "source_id": source_id,
            "target_id": target_id,
            "relation_type": relation_type
        })
        
        rel_id = rel.id
        db.close()
        return rel_id

    @staticmethod
    def get_graph(asset_id):
        db = SessionLocal()
        # Bi-directional search for immediate neighbors
        rels = db.query(Relationship).filter(
            (Relationship.source_id == asset_id) | (Relationship.target_id == asset_id)
        ).all()
        
        nodes = {}
        edges = []
        for r in rels:
            edges.append({"source": r.source_id, "target": r.target_id, "type": r.relation_type})
            
            # Fetch nodes lazy
            for n_id in [r.source_id, r.target_id]:
                if n_id not in nodes:
                    ast = db.query(UniversalAsset).filter(UniversalAsset.id == n_id).first()
                    if ast:
                        nodes[n_id] = {"id": ast.id, "type": ast.asset_type, "value": ast.value, "risk": ast.risk_score}
                        
        db.close()
        return {"nodes": list(nodes.values()), "edges": edges}
