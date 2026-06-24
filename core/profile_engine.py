import json
from core.project_db import SessionLocal, ScanProfile

class ProfileEngine:
    DEFAULT_PROFILES = [
        {
            "name": "Quick Recon",
            "tools": ["subfinder", "dnsx", "httpx"],
            "arguments": {}
        },
        {
            "name": "Deep Recon",
            "tools": ["subfinder", "amass", "dnsx", "httpx", "naabu", "nmap"],
            "arguments": {}
        },
        {
            "name": "Quick Vulnerability",
            "tools": ["nuclei", "sslscan"],
            "arguments": {}
        },
        {
            "name": "Deep Vulnerability",
            "tools": ["nuclei", "nikto", "testssl"],
            "arguments": {}
        },
        {
            "name": "Web Enumeration",
            "tools": ["katana", "ffuf", "linkfinder", "secretfinder"],
            "arguments": {}
        },
        {
            "name": "Cloud Assessment",
            "tools": ["cloud_discovery", "storage", "iam"],
            "arguments": {}
        },
        {
            "name": "Full Assessment",
            "tools": ["subfinder", "dnsx", "httpx", "katana", "ffuf", "nuclei", "cloud_discovery"],
            "arguments": {}
        }
    ]

    @staticmethod
    def seed_profiles():
        db = SessionLocal()
        for p in ProfileEngine.DEFAULT_PROFILES:
            existing = db.query(ScanProfile).filter(ScanProfile.name == p["name"]).first()
            if not existing:
                prof = ScanProfile(
                    name=p["name"],
                    tools=json.dumps(p["tools"]),
                    arguments=json.dumps(p["arguments"]),
                    created_by="system"
                )
                db.add(prof)
        db.commit()
        db.close()

    @staticmethod
    def get_profiles():
        db = SessionLocal()
        profiles = db.query(ScanProfile).all()
        db.close()
        return [{"id": p.id, "name": p.name, "tools": json.loads(p.tools)} for p in profiles]
