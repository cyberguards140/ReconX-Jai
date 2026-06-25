from core.intelligence_db import SessionLocal, UniversalAsset, AssetTag
from intelligence.timeline_engine import TimelineEngine
from dashboard.backend.websocket import broadcast

class RiskEngine:
    @staticmethod
    def calculate_risk(asset_id, findings=None, cloud_exposures=False):
        db = SessionLocal()
        asset = db.query(UniversalAsset).filter(UniversalAsset.id == asset_id).first()
        if not asset:
            db.close()
            return 0
            
        score = 0
        
        # Analyze findings
        findings = findings or []
        for f in findings:
            if f.get('severity') == 'critical':
                score += 50
            elif f.get('severity') == 'high':
                score += 25
            elif f.get('severity') == 'medium':
                score += 10
            elif f.get('severity') == 'low':
                score += 5
                
        if cloud_exposures:
            score += 30
            
        tags = [t.tag.lower() for t in db.query(AssetTag).filter(AssetTag.asset_id == asset_id).all()]
        if 'critical' in tags or 'production' in tags:
            score = min(int(score * 1.5), 100)
            
        score = min(score, 100)
        
        if asset.risk_score != score:
            TimelineEngine.log_event(asset_id, "Risk Changed", f"Risk score updated from {asset.risk_score} to {score}")
            asset.risk_score = score
            db.commit()
            
            broadcast({
                "type": "risk_changed",
                "asset_id": asset_id,
                "new_score": score
            })
            
        db.close()
        return score
