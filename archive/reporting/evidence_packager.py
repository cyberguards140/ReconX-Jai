import os
import shutil
from datetime import datetime
from core.report_db import SessionLocal, EvidencePackage

class EvidencePackager:
    @staticmethod
    def create_package(project_id, project_name):
        print(f"[*] Compiling evidence package for {project_name}...")
        
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'projects', project_name))
        reports_dir = os.path.join(base_dir, 'reports')
        os.makedirs(reports_dir, exist_ok=True)
        
        timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
        zip_path = os.path.join(reports_dir, f"evidence_package_{timestamp}.zip")
        
        # We would collect assets, screenshots, findings, cloud. For now, simulate archiving base_dir.
        shutil.make_archive(zip_path.replace('.zip', ''), 'zip', base_dir)
        
        size = os.path.getsize(zip_path)
        
        db = SessionLocal()
        pkg = EvidencePackage(project_id=project_id, file_path=zip_path, size=size)
        db.add(pkg)
        db.commit()
        db.close()
        
        print(f"[+] Evidence package generated: {zip_path}")
        return zip_path
