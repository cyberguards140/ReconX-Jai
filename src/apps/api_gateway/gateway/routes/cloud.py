from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from apps.api_gateway.dependencies import get_current_identity
from apps.api_gateway.gateway.filtering import FilterParams, get_filter_params
from apps.api_gateway.gateway.pagination import (
    PaginationParams,
    calculate_pagination_meta,
    get_pagination_params,
)
from apps.api_gateway.gateway.responses import PaginatedResponse
from apps.api_gateway.gateway.router_registry import registry
from apps.api_gateway.gateway.search import SearchParams, get_search_params
from apps.api_gateway.gateway.sorting import SortParams, get_sort_params
from core.auth.identity import IdentityContext
from core.auth.middleware import require_permission
from data.database.session import get_db

router = APIRouter()


@router.get("/clusters", response_model=PaginatedResponse)
@require_permission("cloud.read")
async def list_clusters(
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


@router.get("/workloads", response_model=PaginatedResponse)
@require_permission("cloud.read")
async def list_workloads(
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


@router.get("/namespaces", response_model=PaginatedResponse)
@require_permission("cloud.read")
async def list_namespaces(
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


@router.get("/service-mesh", response_model=PaginatedResponse)
@require_permission("cloud.read")
async def list_service_mesh(
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


registry.register(router, prefix="/cloud", version="v1", tags=["Cloud Intelligence"])
