import os

modules = {
    "infra": {"name": "Infrastructure Intelligence", "endpoints": ["asns", "netblocks", "certificates", "organizations"]},
    "events": {"name": "Event Core", "endpoints": ["events", "streams", "subscriptions", "history"]},
    "external": {"name": "External Intelligence", "endpoints": ["exposure", "reputation", "risk-intel"]},
    "visual": {"name": "Visual Intelligence", "endpoints": ["graphs", "topology", "relationships", "metadata"]},
    "threat": {"name": "Threat Intelligence", "endpoints": ["iocs", "actors", "campaigns", "techniques", "detections"]},
    "cloud": {"name": "Cloud Intelligence", "endpoints": ["clusters", "workloads", "namespaces", "service-mesh"]},
    "analytics": {"name": "Security Analytics", "endpoints": ["alerts", "behaviors", "detections", "investigations"]},
    "soc": {"name": "SOC Operations", "endpoints": ["cases", "incidents", "playbooks", "workflows"]},
    "executive": {"name": "Executive Intelligence", "endpoints": ["risk", "compliance", "governance", "portfolio"]}
}

template = """from fastapi import APIRouter, Depends
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

{endpoints}

registry.register(router, prefix="/{module_id}", version="v1", tags=["{module_name}"])
"""

endpoint_template = """@router.get("/{endpoint}", response_model=PaginatedResponse)
@require_permission("{module_id}.read")
async def list_{endpoint_clean}(
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
"""

base_dir = "/home/kali/ReconX/product/src/reconx/api_gateway/routes"
os.makedirs(base_dir, exist_ok=True)

for mod_id, mod_data in modules.items():
    eps = []
    for ep in mod_data["endpoints"]:
        ep_clean = ep.replace("-", "_")
        eps.append(endpoint_template.format(endpoint=ep, endpoint_clean=ep_clean, module_id=mod_id))
        
    content = template.format(
        endpoints="\n".join(eps),
        module_id=mod_id,
        module_name=mod_data["name"]
    )
    
    with open(os.path.join(base_dir, f"{mod_id}.py"), "w") as f:
        f.write(content)
        
print("Routes generated successfully.")
