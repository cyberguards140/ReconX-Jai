from fastapi import Request
from typing import Dict, Any

class FilterParams:
    def __init__(self, filters: Dict[str, Any]):
        self.filters = filters
        
    def to_dict(self) -> Dict[str, Any]:
        return self.filters

def get_filter_params(request: Request) -> FilterParams:
    """
    Extracts all query parameters that aren't standard pagination, sort, or search parameters.
    Supports advanced filtering operations defined by suffixes like __gte, __in, __startswith, etc.
    Example: ?type=domain&risk_score__gte=80
    """
    exclude_params = {"page", "size", "sort", "q", "cursor", "limit"}
    filters = {}
    
    for key, value in request.query_params.multi_items():
        if key not in exclude_params:
            if key in filters:
                if not isinstance(filters[key], list):
                    filters[key] = [filters[key]]
                filters[key].append(value)
            else:
                filters[key] = value
                
    return FilterParams(filters=filters)
