from core.plugin_db import SessionLocal, MarketplacePackage

class MarketplaceEngine:
    @staticmethod
    def fetch_catalog():
        # Simulated remote fetching
        mock_packages = [
            {"package_name": "Advanced OSINT", "version": "2.1", "category": "OSINT", "author": "ReconX Dev", "description": "Extended OSINT gathering via Shodan."},
            {"package_name": "Cloud Enum Pro", "version": "1.0", "category": "Cloud", "author": "Community", "description": "AWS and Azure enumerators."},
            {"package_name": "Dark Enterprise Theme", "version": "1.0", "category": "Themes", "author": "UI Team", "description": "Dark mode theme for SOCs."}
        ]
        
        db = SessionLocal()
        for pkg in mock_packages:
            existing = db.query(MarketplacePackage).filter(MarketplacePackage.package_name == pkg["package_name"]).first()
            if not existing:
                p = MarketplacePackage(**pkg)
                db.add(p)
        db.commit()
        db.close()
        
        db = SessionLocal()
        catalog = db.query(MarketplacePackage).all()
        res = [{"id": c.id, "name": c.package_name, "version": c.version, "category": c.category} for c in catalog]
        db.close()
        return res
