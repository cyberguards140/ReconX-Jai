from typing import Optional
from fastapi import Query
from pydantic import BaseModel

class SearchParams(BaseModel):
    q: Optional[str] = None

def get_search_params(
    q: Optional[str] = Query(None, description="Search query string for full-text search")
) -> SearchParams:
    """
    Extracts global search parameters.
    Example: ?q=google.com
    """
    return SearchParams(q=q)
