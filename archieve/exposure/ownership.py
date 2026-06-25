from core.exposure_db import SessionLocal, Ownership
from dashboard.backend.websocket import broadcast

class OwnershipEngine:
    @staticmethod
    def assign_owner(asset_id, owner_team):
        db = SessionLocal()
        o = db.query(Ownership).filter_by(asset_id=asset_id).first()
        if not o:
            o = Ownership(asset_id=asset_id, owner=owner_team)
            db.add(o)
        else:
            o.owner = owner_team
        db.commit()
        
        broadcast({"type": "owner_assigned", "asset_id": asset_id, "owner": owner_team})
        db.close()
        return True
