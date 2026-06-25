from core.threat_db import SessionLocal, CVEData
from dashboard.backend.websocket import broadcast

class CVEEngine:
    # Simulated CPE-to-CVE mapping logic
    MOCK_MAPPINGS = {
        "apache 2.4.49": {"cve": "CVE-2021-41773", "severity": "critical", "cvss": 9.8},
        "log4j": {"cve": "CVE-2021-44228", "severity": "critical", "cvss": 10.0},
        "wordpress 5.2": {"cve": "CVE-2019-16219", "severity": "high", "cvss": 8.0}
    }

    @staticmethod
    def map_technology(asset_id, technology_string):
        technology_lower = technology_string.lower()
        db = SessionLocal()
        
        correlated = False
        for key, vuln in CVEEngine.MOCK_MAPPINGS.items():
            if key in technology_lower:
                cve_obj = CVEData(
                    asset_id=asset_id, 
                    cve=vuln["cve"], 
                    severity=vuln["severity"], 
                    cvss=vuln["cvss"]
                )
                db.add(cve_obj)
                db.commit()
                
                broadcast({
                    "type": "new_cve_correlated",
                    "asset_id": asset_id,
                    "cve": vuln["cve"],
                    "severity": vuln["severity"]
                })
                correlated = True
                
        db.close()
        return correlated
