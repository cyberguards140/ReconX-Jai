from core.asset_db import SessionLocal, Asset, Relationship, AssetHistory
from core.event_engine import EventEngine
from datetime import datetime

class InventoryManager:
    @staticmethod
    def get_or_create_asset(asset_type, value, project_id, source):
        db = SessionLocal()
        asset = db.query(Asset).filter(
            Asset.asset_type == asset_type, 
            Asset.value == value, 
            Asset.project_id == project_id
        ).first()
        
        is_new = False
        if asset:
            asset.last_seen = datetime.utcnow()
            asset.source = source # Update source or append
            db.commit()
            db.refresh(asset)
            EventEngine.publish_asset_updated(asset_type, value, project_id, source)
        else:
            asset = Asset(
                asset_type=asset_type,
                value=value,
                project_id=project_id,
                source=source
            )
            db.add(asset)
            db.commit()
            db.refresh(asset)
            
            # Log history
            history = AssetHistory(asset_id=asset.id, event_description="Discovered")
            db.add(history)
            db.commit()
            
            is_new = True
            EventEngine.publish_new_asset(asset_type, value, project_id, source)
            
        res = asset.id
        db.close()
        return res, is_new

    @staticmethod
    def create_relationship(source_id, target_id, relation_type):
        db = SessionLocal()
        rel = db.query(Relationship).filter(
            Relationship.source_id == source_id,
            Relationship.target_id == target_id,
            Relationship.relation_type == relation_type
        ).first()
        
        if not rel:
            rel = Relationship(source_id=source_id, target_id=target_id, relation_type=relation_type)
            db.add(rel)
            db.commit()
            
        db.close()

    @staticmethod
    def get_assets_by_project(project_id, asset_type=None):
        db = SessionLocal()
        q = db.query(Asset).filter(Asset.project_id == project_id)
        if asset_type:
            q = q.filter(Asset.asset_type == asset_type)
        assets = q.all()
        res = [{"id": a.id, "type": a.asset_type, "value": a.value, "source": a.source, "last_seen": a.last_seen.isoformat()} for a in assets]
        db.close()
        return res

    @staticmethod
    def get_stats(project_id):
        db = SessionLocal()
        domains = db.query(Asset).filter(Asset.project_id == project_id, Asset.asset_type == 'domain').count()
        subdomains = db.query(Asset).filter(Asset.project_id == project_id, Asset.asset_type == 'subdomain').count()
        ports = db.query(Asset).filter(Asset.project_id == project_id, Asset.asset_type == 'port').count()
        services = db.query(Asset).filter(Asset.project_id == project_id, Asset.asset_type == 'service').count()
        db.close()
        return {
            "domains": domains,
            "subdomains": subdomains,
            "ports": ports,
            "services": services
        }
