from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse, PlainTextResponse
from sqlalchemy.orm import Session

from apps.api_gateway.gateway.router_registry import registry
from attack_surface.assets.analytics import AnalyticsEngine
from data.database.session import get_db

router = APIRouter()
registry.register(router, prefix="/reports", version="v1", tags=["reports"])


@router.get("/export")
async def export_report(
    project_id: str = "default", format: str = "json", db: Session = Depends(get_db)
):
    """
    Generates a full compliance/status report in JSON or Markdown format.
    """
    overview = AnalyticsEngine.get_attack_surface_overview(db, project_id)

    # In a full implementation, we would query the VulnerabilityManager / Database for findings here too
    report_data = {
        "project_id": project_id,
        "attack_surface": overview,
        # "findings": db.query(Finding).all()
    }

    if format == "json":
        return JSONResponse(content=report_data)
    elif format == "markdown":
        md = "# ReconX Security Report\n\n## Attack Surface\n"
        for k, v in overview.items():
            md += f"- **{k.title()}**: {v}\n"
        return PlainTextResponse(content=md, media_type="text/markdown")
    else:
        return {"error": "Unsupported format. Use 'json' or 'markdown'."}


@router.get("/compliance/{framework}")
async def get_compliance_report(framework: str, db: Session = Depends(get_db)):
    """
    Generates an ISO27001 or SOC2 compliance gap report.
    """
    from reporting.compliance_mapper import compliance_mapper

    # In a real system, query the DB for findings and exposures
    mock_findings = [
        {"title": "SQL Injection", "asset_target": "api.example.com", "severity": "critical"}
    ]
    mock_exposures = [
        {"target": "vpn.example.com", "is_critical_exposure": True, "exposure_tags": ["VPN Portal"]}
    ]

    report_md = compliance_mapper.generate_gap_report(framework, mock_findings, mock_exposures)

    if report_md.startswith("# Error"):
        raise HTTPException(status_code=400, detail="Unsupported Framework")

    return PlainTextResponse(content=report_md, media_type="text/markdown")


@router.get("/")
async def get_reports():
    return {"status": "ok", "service": "reports"}
