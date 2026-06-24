from core.intelligence_db import SessionLocal, UniversalAsset, AssetSearchIndex
from sqlalchemy import or_

class SearchEngine:
    @staticmethod
    def index_asset(asset_id, text):
        db = SessionLocal()
        idx = db.query(AssetSearchIndex).filter(AssetSearchIndex.asset_id == asset_id).first()
        if not idx:
            idx = AssetSearchIndex(asset_id=asset_id, searchable_text=text.lower())
            db.add(idx)
        else:
            idx.searchable_text = text.lower()
        db.commit()
        db.close()

    @staticmethod
    def search(query):
        db = SessionLocal()
        query = query.lower()
        
        # Simple string matching across UniversalAsset and SearchIndex
        results = db.query(UniversalAsset).outerjoin(
            AssetSearchIndex, UniversalAsset.id == AssetSearchIndex.asset_id
        ).filter(
            or_(
                UniversalAsset.value.ilike(f"%{query}%"),
                UniversalAsset.asset_type.ilike(f"%{query}%"),
                AssetSearchIndex.searchable_text.ilike(f"%{query}%")
            )
        ).all()
        
        out = [{"id": r.id, "type": r.asset_type, "value": r.value, "risk": r.risk_score} for r in results]
        db.close()
        return out
