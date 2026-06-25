from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from reconx.api.dependencies import get_current_user, require_admin
from reconx.enterprise.organizations.organization_service import OrganizationService
from reconx.enterprise.tenants.tenant_manager import TenantManager

router = APIRouter(prefix="/tenants", tags=["Tenants"])
tenant_manager = TenantManager()
org_service = OrganizationService()


class TenantCreateRequest(BaseModel):
    name: str
    billing_plan: str = "Enterprise"


class TenantStatusUpdate(BaseModel):
    status: str


class OrganizationCreateRequest(BaseModel):
    name: str
    description: str = None


@router.post("", response_model=dict[str, Any])
async def create_tenant(req: TenantCreateRequest, current_user: Any = Depends(require_admin)):
    """Creates a new Tenant (Enterprise/MSSP). Super Admin only in a real deployment."""
    try:
        tenant = await tenant_manager.create_tenant(req.name, req.billing_plan)
        return {"status": "success", "tenant": tenant}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("", response_model=list[dict[str, Any]])
async def list_tenants(current_user: Any = Depends(require_admin)):
    """Lists all tenants."""
    return await tenant_manager.list_tenants()


@router.get("/{tenant_id}", response_model=dict[str, Any])
async def get_tenant(tenant_id: str, current_user: Any = Depends(get_current_user)):
    """Retrieves tenant details."""
    tenant = await tenant_manager.get_tenant(tenant_id)
    if not tenant:
        raise HTTPException(status_code=404, detail="Tenant not found")
    return tenant


@router.put("/{tenant_id}/status", response_model=dict[str, Any])
async def update_tenant_status(
    tenant_id: str, req: TenantStatusUpdate, current_user: Any = Depends(require_admin)
):
    """Updates tenant status (ACTIVE, SUSPENDED, etc)."""
    try:
        success = await tenant_manager.update_tenant_status(tenant_id, req.status)
        if not success:
            raise HTTPException(status_code=404, detail="Tenant not found")
        return {"status": "success", "new_status": req.status}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/{tenant_id}/organizations", response_model=dict[str, Any])
async def create_organization(
    tenant_id: str, req: OrganizationCreateRequest, current_user: Any = Depends(require_admin)
):
    """Creates an organization hierarchy under a tenant."""
    org_id = await org_service.create_organization(req.name, tenant_id, req.description)
    return {"status": "success", "organization_id": org_id}


@router.get("/{tenant_id}/hierarchy", response_model=list[dict[str, Any]])
async def get_hierarchy(tenant_id: str, current_user: Any = Depends(get_current_user)):
    """Retrieves the full organization hierarchy for a tenant."""
    return await org_service.get_organization_hierarchy(tenant_id)
