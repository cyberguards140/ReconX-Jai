from fastapi import APIRouter, Depends
from typing import List, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from apps.api_gateway.gateway.router_registry import registry
from data.database.repositories.finding import finding_repo
from data.database.models import Finding, SeverityEnum
from data.database.session import get_db

router = APIRouter()
registry.register(router, prefix="/findings", version="v1", tags=["findings"])

@router.get("/")
async def get_findings(db: AsyncSession = Depends(get_db)):
    """Returns actual findings from the database."""
    findings = await finding_repo.get_multi(db)
    out = []
    for f in findings:
        out.append({
            "id": f.id,
            "title": f.title,
            "severity": f.severity.value if hasattr(f.severity, 'value') else f.severity,
            "description": f.capability if hasattr(f, 'capability') else '',
            "source_tool": f.source if hasattr(f, 'source') else 'System',
            "scan_id": f.scan_id,
            "asset_id": f.asset_id
        })
    return out
