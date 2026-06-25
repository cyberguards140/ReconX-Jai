from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from apps.api_gateway.dependencies import get_current_identity
from apps.api_gateway.gateway.filtering import FilterParams, get_filter_params
from apps.api_gateway.gateway.pagination import (
    PaginationParams,
    calculate_pagination_meta,
    get_pagination_params,
)
from apps.api_gateway.gateway.responses import PaginatedResponse, SuccessResponse
from apps.api_gateway.gateway.router_registry import registry
from apps.api_gateway.gateway.search import SearchParams, get_search_params
from apps.api_gateway.gateway.sorting import SortParams, get_sort_params
from core.auth.identity import IdentityContext
from core.auth.middleware import require_permission
from data.database.session import get_db
from recon.services.intelligence.intelligence_store import IntelligenceStore

router = APIRouter()


@router.get("/assets", response_model=PaginatedResponse)
@require_permission("asset.read")
async def list_assets(
    pagination: PaginationParams = Depends(get_pagination_params),
    filters: FilterParams = Depends(get_filter_params),
    sort: SortParams = Depends(get_sort_params),
    search: SearchParams = Depends(get_search_params),
    db: AsyncSession = Depends(get_db),
    identity: IdentityContext = Depends(get_current_identity),
):
    store = IntelligenceStore(db)
    all_assets = await store.get_assets()

    if search.q:
        all_assets = [a for a in all_assets if search.q.lower() in str(a).lower()]

    total = len(all_assets)
    paginated = all_assets[pagination.offset : pagination.offset + pagination.limit]
    meta = calculate_pagination_meta(pagination.page, pagination.size, total)
    return PaginatedResponse(data=paginated, meta=meta)


@router.get("/assets/{id}", response_model=SuccessResponse)
@require_permission("asset.read")
async def get_asset(
    id: str,
    db: AsyncSession = Depends(get_db),
    identity: IdentityContext = Depends(get_current_identity),
):
    store = IntelligenceStore(db)
    all_assets = await store.get_assets()
    asset = next((a for a in all_assets if str(a.get("id")) == id), None)
    if not asset:
        from apps.api_gateway.gateway.exceptions import ResourceNotFoundException

        raise ResourceNotFoundException("Asset not found")
    return SuccessResponse(data=asset)


@router.post("/assets", response_model=SuccessResponse)
@require_permission("asset.create")
async def create_asset(
    asset_data: dict,
    db: AsyncSession = Depends(get_db),
    identity: IdentityContext = Depends(get_current_identity),
):
    from data.database.repositories.asset import asset_repo

    new_asset = await asset_repo.create(db, obj_in={**asset_data, "project_id": identity.tenant_id})
    return SuccessResponse(data={"id": new_asset.id})


registry.register(router, prefix="/asm", version="v1", tags=["ASM Core"])
