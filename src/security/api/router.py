from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status

from core.auth.middleware import SecurityMiddleware
from security.compliance.mapper import ComplianceMapper

router = APIRouter(tags=["Security"], dependencies=[Depends(SecurityMiddleware)])


@router.get("/compliance/{framework}", summary="Get Compliance Readiness")
async def get_compliance_status(framework: str) -> dict[str, Any]:
    """
    Retrieves the compliance control mapping for a specific framework (e.g., SOC2, ISO27001).
    Used to automatically generate evidence reports for auditors.
    """
    try:
        return ComplianceMapper.get_framework_status(framework)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get("/compliance", summary="Get All Compliance Mappings")
async def get_all_compliance() -> dict[str, Any]:
    """
    Retrieves all mapped compliance frameworks for the ReconX Platform.
    """
    return ComplianceMapper.get_all_mappings()


# Note: /audit, /events, /policies would connect to their respective stores/DB tables.
