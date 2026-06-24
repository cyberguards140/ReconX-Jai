from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from reconx.database.session import get_db
from reconx.api.dependencies import get_current_identity
from reconx.auth.identity import IdentityContext
from reconx.auth.middleware import require_permission
from reconx.api_gateway.responses import SuccessResponse, PaginatedResponse
from reconx.api_gateway.pagination import get_pagination_params, calculate_pagination_meta, PaginationParams
from reconx.api_gateway.filtering import get_filter_params, FilterParams
from reconx.api_gateway.sorting import get_sort_params, SortParams
from reconx.api_gateway.search import get_search_params, SearchParams
from reconx.api_gateway.router_registry import registry

router = APIRouter()

@router.get("/asns", response_model=PaginatedResponse)
@require_permission("infra.read")
async def list_asns(
    pagination: PaginationParams = Depends(get_pagination_params),
    filters: FilterParams = Depends(get_filter_params),
    sort: SortParams = Depends(get_sort_params),
    search: SearchParams = Depends(get_search_params),
    db: AsyncSession = Depends(get_db), 
    identity: IdentityContext = Depends(get_current_identity)
):
    # Dummy DB query
    items = []
    meta = calculate_pagination_meta(pagination.page, pagination.size, len(items))
    return PaginatedResponse(data=items, meta=meta)

@router.get("/netblocks", response_model=PaginatedResponse)
@require_permission("infra.read")
async def list_netblocks(
    pagination: PaginationParams = Depends(get_pagination_params),
    filters: FilterParams = Depends(get_filter_params),
    sort: SortParams = Depends(get_sort_params),
    search: SearchParams = Depends(get_search_params),
    db: AsyncSession = Depends(get_db), 
    identity: IdentityContext = Depends(get_current_identity)
):
    # Dummy DB query
    items = []
    meta = calculate_pagination_meta(pagination.page, pagination.size, len(items))
    return PaginatedResponse(data=items, meta=meta)

@router.get("/certificates", response_model=PaginatedResponse)
@require_permission("infra.read")
async def list_certificates(
    pagination: PaginationParams = Depends(get_pagination_params),
    filters: FilterParams = Depends(get_filter_params),
    sort: SortParams = Depends(get_sort_params),
    search: SearchParams = Depends(get_search_params),
    db: AsyncSession = Depends(get_db), 
    identity: IdentityContext = Depends(get_current_identity)
):
    # Dummy DB query
    items = []
    meta = calculate_pagination_meta(pagination.page, pagination.size, len(items))
    return PaginatedResponse(data=items, meta=meta)

@router.get("/organizations", response_model=PaginatedResponse)
@require_permission("infra.read")
async def list_organizations(
    pagination: PaginationParams = Depends(get_pagination_params),
    filters: FilterParams = Depends(get_filter_params),
    sort: SortParams = Depends(get_sort_params),
    search: SearchParams = Depends(get_search_params),
    db: AsyncSession = Depends(get_db), 
    identity: IdentityContext = Depends(get_current_identity)
):
    # Dummy DB query
    items = []
    meta = calculate_pagination_meta(pagination.page, pagination.size, len(items))
    return PaginatedResponse(data=items, meta=meta)


registry.register(router, prefix="/infra", version="v1", tags=["Infrastructure Intelligence"])
