from core.threat_db import SessionLocal, PassiveDNS

class PassiveDNSEngine:
    @staticmethod
    def query(domain):
        # Simulated Passive DNS lookup
        mock_data = {
            "example.com": ["93.184.216.34", "93.184.216.35"]
        }
        
        historical_ips = mock_data.get(domain, [])
        db = SessionLocal()
        
        for ip in historical_ips:
            pdns = PassiveDNS(domain=domain, historical_ip=ip)
            db.add(pdns)
            
        db.commit()
        db.close()
        return historical_ips
