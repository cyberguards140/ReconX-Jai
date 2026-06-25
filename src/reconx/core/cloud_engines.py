from core.cloud_db import SessionLocal, CloudAsset, StorageBucket, IAMEntity, PublicExposure, CloudRelationship
from dashboard.backend.websocket import broadcast
from datetime import datetime

class CloudEngines:
    @staticmethod
    def store_cloud_asset(project_id, provider, service, resource_type, name, public=False):
        db = SessionLocal()
        existing = db.query(CloudAsset).filter(
            CloudAsset.project_id == project_id,
            CloudAsset.provider == provider,
            CloudAsset.name == name
        ).first()

        is_new = False
        if existing:
            existing.last_seen = datetime.utcnow()
            asset_id = existing.id
            db.commit()
        else:
            asset = CloudAsset(
                provider=provider,
                service=service,
                resource_type=resource_type,
                name=name,
                public=public,
                project_id=project_id
            )
            db.add(asset)
            db.commit()
            db.refresh(asset)
            asset_id = asset.id
            is_new = True

        db.close()
        
        if is_new:
            msg = {
                "type": "new_cloud_asset",
                "provider": provider,
                "name": name,
                "project_id": project_id
            }
            broadcast(msg)
            
        return asset_id, is_new

    @staticmethod
    def log_public_exposure(project_id, asset_id, finding, severity):
        db = SessionLocal()
        existing = db.query(PublicExposure).filter(
            PublicExposure.project_id == project_id,
            PublicExposure.asset_id == asset_id,
            PublicExposure.finding == finding
        ).first()

        if not existing:
            exp = PublicExposure(
                asset_id=asset_id,
                finding=finding,
                severity=severity,
                project_id=project_id
            )
            db.add(exp)
            db.commit()
            
            msg = {
                "type": "public_exposure",
                "severity": severity,
                "finding": finding,
                "project_id": project_id
            }
            broadcast(msg)
        db.close()

    @staticmethod
    def store_storage_bucket(project_id, provider, name, public=False, object_count=0):
        db = SessionLocal()
        existing = db.query(StorageBucket).filter(
            StorageBucket.project_id == project_id,
            StorageBucket.name == name
        ).first()

        if not existing:
            bucket = StorageBucket(
                provider=provider,
                name=name,
                public=public,
                object_count=object_count,
                project_id=project_id
            )
            db.add(bucket)
            db.commit()
        else:
            existing.object_count = object_count
            existing.public = public
            db.commit()
        db.close()

    @staticmethod
    def store_iam_entity(project_id, provider, entity_type, name):
        db = SessionLocal()
        existing = db.query(IAMEntity).filter(
            IAMEntity.project_id == project_id,
            IAMEntity.name == name,
            IAMEntity.entity_type == entity_type
        ).first()

        if not existing:
            entity = IAMEntity(
                provider=provider,
                entity_type=entity_type,
                name=name,
                project_id=project_id
            )
            db.add(entity)
            db.commit()
        db.close()
