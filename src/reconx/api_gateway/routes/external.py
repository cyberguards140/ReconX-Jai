from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from reconx.api.dependencies import get_current_identity
from reconx.api_gateway.filtering import FilterParams, get_filter_params
from reconx.api_gateway.pagination import (
    PaginationParams,
    calculate_pagination_meta,
    get_pagination_params,
)
from reconx.api_gateway.responses import PaginatedResponse
from reconx.api_gateway.router_registry import registry
from reconx.api_gateway.search import SearchParams, get_search_params
from reconx.api_gateway.sorting import SortParams, get_sort_params
from reconx.auth.identity import IdentityContext
from reconx.auth.middleware import require_permission
from reconx.database.session import get_db

router = APIRouter()


@router.get("/exposure", response_model=PaginatedResponse)
@require_permission("external.read")
async def list_exposure(
    pagination: PaginationParams = Depends(get_pagination_params),
    filters: FilterParams = Depends(get_filter_params),
    sort: SortParams = Depends(get_sort_params),
    search: SearchParams = Depends(get_search_params),
    db: AsyncSession = Depends(get_db),
    identity: IdentityContext = Depends(get_current_identity),
):
    # Dummy DB query
    items = []
    meta = calculate_pagination_meta(pagination.page, pagination.size, len(items))
    return PaginatedResponse(data=items, meta=meta)


@router.get("/reputation", response_model=PaginatedResponse)
@require_permission("external.read")
async def list_reputation(
    pagination: PaginationParams = Depends(get_pagination_params),
    filters: FilterParams = Depends(get_filter_params),
    sort: SortParams = Depends(get_sort_params),
    search: SearchParams = Depends(get_search_params),
    db: AsyncSession = Depends(get_db),
    identity: IdentityContext = Depends(get_current_identity),
):
    # Dummy DB query
    items = []
    meta = calculate_pagination_meta(pagination.page, pagination.size, len(items))
    return PaginatedResponse(data=items, meta=meta)


@router.get("/risk-intel", response_model=PaginatedResponse)
@require_permission("external.read")
async def list_risk_intel(
    pagination: PaginationParams = Depends(get_pagination_params),
    filters: FilterParams = Depends(get_filter_params),
    sort: SortParams = Depends(get_sort_params),
    search: SearchParams = Depends(get_search_params),
    db: AsyncSession = Depends(get_db),
    identity: IdentityContext = Depends(get_current_identity),
):
    # Dummy DB query
    items = []
    meta = calculate_pagination_meta(pagination.page, pagination.size, len(items))
    return PaginatedResponse(data=items, meta=meta)


registry.register(router, prefix="/external", version="v1", tags=["External Intelligence"])
