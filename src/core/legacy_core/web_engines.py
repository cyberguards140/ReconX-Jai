from core.legacy_core.web_db import SessionLocal, WebAsset, Secret, Technology, WebRelationship
from dashboard.backend.websocket import broadcast
from datetime import datetime
import uuid

class WebEngines:
    @staticmethod
    def store_web_asset(project_id, host, asset_type, value, source, status=None):
        db = SessionLocal()
        existing = db.query(WebAsset).filter(
            WebAsset.project_id == project_id,
            WebAsset.host == host,
            WebAsset.value == value,
            WebAsset.asset_type == asset_type
        ).first()

        is_new = False
        if existing:
            existing.last_seen = datetime.utcnow()
            if status is not None:
                existing.status = status
            asset_id = existing.id
            db.commit()
        else:
            asset = WebAsset(
                asset_type=asset_type,
                value=value,
                source=source,
                host=host,
                project_id=project_id,
                status=status
            )
            db.add(asset)
            db.commit()
            db.refresh(asset)
            asset_id = asset.id
            is_new = True

        db.close()
        
        if is_new:
            msg = {
                "type": "new_web_asset",
                "asset_type": asset_type,
                "value": value,
                "project_id": project_id,
                "source": source
            }
            broadcast(msg)
            
        return asset_id, is_new

    @staticmethod
    def store_secret(project_id, category, value, source_url_id=None):
        db = SessionLocal()
        existing = db.query(Secret).filter(
            Secret.project_id == project_id,
            Secret.value == value
        ).first()

        if not existing:
            sec = Secret(
                category=category,
                value=value,
                source_id=source_url_id,
                project_id=project_id
            )
            db.add(sec)
            db.commit()
            
            msg = {
                "type": "new_secret",
                "category": category,
                "project_id": project_id
            }
            broadcast(msg)
        db.close()

    @staticmethod
    def store_technology(project_id, host, name):
        db = SessionLocal()
        existing = db.query(Technology).filter(
            Technology.project_id == project_id,
            Technology.host == host,
            Technology.name == name
        ).first()

        if not existing:
            tech = Technology(
                name=name,
                host=host,
                project_id=project_id
            )
            db.add(tech)
            db.commit()
            
            msg = {
                "type": "new_technology",
                "name": name,
                "project_id": project_id,
                "host": host
            }
            broadcast(msg)
        db.close()

    @staticmethod
    def create_relationship(source_id, target_id):
        db = SessionLocal()
        rel = db.query(WebRelationship).filter(
            WebRelationship.source_id == source_id,
            WebRelationship.target_id == target_id
        ).first()
        if not rel:
            rel = WebRelationship(source_id=source_id, target_id=target_id)
            db.add(rel)
            db.commit()
        db.close()
