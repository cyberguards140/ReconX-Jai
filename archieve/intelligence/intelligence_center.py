from core.intelligence_db import SessionLocal, UniversalAsset
from intelligence.relationship_engine import RelationshipEngine
from intelligence.risk_engine import RiskEngine
from intelligence.timeline_engine import TimelineEngine
from intelligence.search_engine import SearchEngine
from dashboard.backend.websocket import broadcast

class IntelligenceCenter:
    @staticmethod
    def register_asset(project_id, asset_type, value):
        db = SessionLocal()
        asset = db.query(UniversalAsset).filter(
            UniversalAsset.project_id == project_id,
            UniversalAsset.asset_type == asset_type,
            UniversalAsset.value == value
        ).first()
        
        if not asset:
            asset = UniversalAsset(project_id=project_id, asset_type=asset_type, value=value)
            db.add(asset)
            db.commit()
            db.refresh(asset)
            
            TimelineEngine.log_event(asset.id, "Asset Discovered", f"New {asset_type} discovered: {value}")
            SearchEngine.index_asset(asset.id, f"{asset_type} {value}")
            
            broadcast({
                "type": "new_asset",
                "asset_id": asset.id,
                "asset_type": asset_type,
                "value": value
            })
            
        asset_id = asset.id
        db.close()
        return asset_id

    @staticmethod
    def process_correlation(source_asset_id, target_asset_id, relationship_type, findings=None):
        rel_id = RelationshipEngine.link_assets(source_asset_id, target_asset_id, relationship_type)
        if findings:
            RiskEngine.calculate_risk(target_asset_id, findings=findings)
        return rel_id

    @staticmethod
    def get_asset_profile(asset_id):
        db = SessionLocal()
        asset = db.query(UniversalAsset).filter(UniversalAsset.id == asset_id).first()
        if not asset:
            db.close()
            return None
            
        profile = {
            "id": asset.id,
            "type": asset.asset_type,
            "value": asset.value,
            "risk": asset.risk_score,
            "graph": RelationshipEngine.get_graph(asset_id)
        }
        db.close()
        return profile
