import os
import uuid
from datetime import datetime, timezone
from typing import Any

from data.database.models import ReportRecord
from reporting.engine.exporter import DataExporter
from reporting.engine.renderer import get_renderer


class ReportEngine:
    def __init__(self, templates_dir: str):
        self.templates_dir = templates_dir
        self.renderer = get_renderer(templates_dir)

    async def generate_executive_report(
        self,
        session,
        target_scope: str,
        title: str = "Executive Summary",
        export_format: str = "pdf",
        report_data: dict[str, Any] | None = None,
    ) -> ReportRecord:
        """
        Generate an Executive Briefing report.
        """
        # In a real scenario, this data would be fetched from the DB based on target_scope.
        # For now, we will use provided report_data or mock it.
        context = (
            {
                "title": title,
                "generated_at": datetime.now(timezone.utc),
                "target_scope": target_scope,
                "summary": report_data.get(
                    "summary",
                    "This report provides an executive overview of the security posture for the specified scope.",
                ),
                "risk_score": report_data.get("risk_score", 45),
                "critical_findings_count": report_data.get("critical_findings_count", 0),
                "total_assets": report_data.get("total_assets", 0),
                "findings": report_data.get("findings", []),
                "recommendations": report_data.get(
                    "recommendations",
                    ["Implement strict access controls", "Patch critical vulnerabilities"],
                ),
            }
            if report_data
            else {
                "title": title,
                "generated_at": datetime.now(timezone.utc),
                "target_scope": target_scope,
                "summary": "No data provided.",
                "risk_score": 0,
                "critical_findings_count": 0,
                "total_assets": 0,
                "findings": [],
                "recommendations": [],
            }
        )

        # Generate output
        record_id = str(uuid.uuid4())

        output_content = None
        if export_format == "pdf":
            output_content = self.renderer.render_pdf("executive.html", context)
        elif export_format == "html":
            output_content = self.renderer.render_html("executive.html", context).encode("utf-8")
        elif export_format == "json":
            output_content = DataExporter.export_json(context).encode("utf-8")
        else:
            raise ValueError(f"Unsupported export format: {export_format}")

        # Ensure reports dir exists
        reports_dir = os.path.join(os.path.dirname(self.templates_dir), "reports")
        os.makedirs(reports_dir, exist_ok=True)

        file_path = os.path.join(reports_dir, f"{record_id}.{export_format}")
        with open(file_path, "wb") as f:
            f.write(output_content)

        # Create DB Record
        record = ReportRecord(
            id=record_id,
            report_id=record_id,
            report_type="Executive",
            title=title,
            generated_at=datetime.now(timezone.utc).isoformat(),
            metadata_json={
                "target_scope": target_scope,
                "format": export_format,
                "file_path": file_path,
            },
        )
        session.add(record)
        await session.commit()
        await session.refresh(record)

        return record

    async def generate_technical_report(
        self,
        session,
        target_scope: str,
        title: str = "Technical Report",
        export_format: str = "json",
        report_data: dict[str, Any] | None = None,
    ) -> ReportRecord:
        """
        Generate a detailed Technical Report, primarily JSON/CSV.
        """
        record_id = str(uuid.uuid4())
        reports_dir = os.path.join(os.path.dirname(self.templates_dir), "reports")
        os.makedirs(reports_dir, exist_ok=True)

        data = report_data.get("data", []) if report_data else []
        file_path = os.path.join(reports_dir, f"{record_id}.{export_format}")

        if export_format == "json":
            content = DataExporter.export_json(data).encode("utf-8")
        elif export_format == "csv":
            content = DataExporter.export_csv(data).encode("utf-8")
        else:
            raise ValueError(f"Unsupported technical report format: {export_format}")

        with open(file_path, "wb") as f:
            f.write(content)

        record = ReportRecord(
            id=record_id,
            report_id=record_id,
            report_type="Technical",
            title=title,
            generated_at=datetime.now(timezone.utc).isoformat(),
            metadata_json={
                "target_scope": target_scope,
                "format": export_format,
                "file_path": file_path,
            },
        )
        session.add(record)
        await session.commit()
        await session.refresh(record)

        return record
