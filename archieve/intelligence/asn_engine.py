from core.threat_db import SessionLocal, ASNData

class ASNEngine:
    @staticmethod
    def enrich_ip(asset_id, ip_address):
        # Simulated ASN lookups
        lookup_table = {
            "104.21.5.5": {"asn": "AS13335", "organization": "Cloudflare", "country": "US"},
            "8.8.8.8": {"asn": "AS15169", "organization": "Google LLC", "country": "US"}
        }
        
        data = lookup_table.get(ip_address, {"asn": "AS00000", "organization": "Unknown ISP", "country": "Unknown"})
        
        db = SessionLocal()
        asn = ASNData(
            asset_id=asset_id,
            asn=data["asn"],
            organization=data["organization"],
            country=data["country"]
        )
        db.add(asn)
        db.commit()
        db.close()
        return data
