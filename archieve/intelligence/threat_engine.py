from core.threat_db import SessionLocal, IOCData, ReputationData
from dashboard.backend.websocket import broadcast

class ThreatEngine:
    @staticmethod
    def analyze_asset(asset_id, asset_type, value):
        # Simulate IOC feed matching
        malicious_ips = ["1.2.3.4", "185.15.5.5"]
        malicious_domains = ["evil.com", "c2.example.com"]
        
        is_malicious = False
        
        if asset_type == "ip" and value in malicious_ips:
            is_malicious = True
        elif asset_type == "domain" and value in malicious_domains:
            is_malicious = True
            
        db = SessionLocal()
        if is_malicious:
            ioc = IOCData(asset_id=asset_id, ioc_type=asset_type, value=value, source="Simulated Threat Feed")
            db.add(ioc)
            
            rep = ReputationData(asset_id=asset_id, reputation_score=10.0, status="malicious")
            db.add(rep)
            db.commit()
            
            broadcast({
                "type": "ioc_match_found",
                "asset_id": asset_id,
                "value": value
            })
        else:
            rep = ReputationData(asset_id=asset_id, reputation_score=95.0, status="trusted")
            db.add(rep)
            db.commit()
            
        db.close()
        return is_malicious
