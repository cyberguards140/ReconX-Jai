import os
from datetime import datetime
from core.report_db import SessionLocal, Report, ReportHistory
from reporting.markdown_generator import MarkdownGenerator
from reporting.pdf_generator import PDFGenerator

class ReportEngine:
    @staticmethod
    def generate_report(project_id, project_name, report_type):
        print(f"[*] Compiling data for {report_type} report on project {project_name}...")
        
        # In a real environment, query finding_db, assets_db, cloud_db here.
        # For this framework, we aggregate mock data representing the database states.
        
        data = {
            "project_name": project_name,
            "date": datetime.utcnow().strftime("%Y-%m-%d"),
            "report_type": report_type.capitalize(),
            "stats": {
                "critical": 1,
                "high": 3,
                "medium": 5,
                "low": 12,
                "info": 40,
                "domains": 5,
                "cloud_exposures": 0
            },
            "findings": [
                {"title": "Open Directory", "severity": "High", "asset": "files.example.com"}
            ]
        }
        
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'projects', project_name, 'reports'))
        os.makedirs(base_dir, exist_ok=True)
        
        # Determine versions
        db = SessionLocal()
        existing_count = db.query(Report).filter(Report.project_id == project_id, Report.report_type == report_type).count()
        version = existing_count + 1
        
        md_path = os.path.join(base_dir, f"{report_type}_v{version}.md")
        pdf_path = os.path.join(base_dir, f"{report_type}_v{version}.pdf")
        
        # Generate formats
        MarkdownGenerator.generate(data, md_path)
        PDFGenerator.generate(md_path, pdf_path)
        
        rep = Report(
            project_id=project_id,
            report_type=report_type,
            version=version,
            file_path=pdf_path
        )
        db.add(rep)
        db.commit()
        db.refresh(rep)
        
        hist = ReportHistory(report_id=rep.id, action="generated")
        db.add(hist)
        db.commit()
        
        rep_id = rep.id
        db.close()
        
        print(f"[+] Report generated at {pdf_path}")
        return rep_id
