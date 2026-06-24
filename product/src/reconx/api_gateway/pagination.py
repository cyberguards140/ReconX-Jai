from typing import Optional, Dict
from fastapi import Query
from pydantic import BaseModel

class PaginationParams(BaseModel):
    page: int = 1
    size: int = 50
    
    @property
    def offset(self) -> int:
        return (self.page - 1) * self.size
    
    @property
    def limit(self) -> int:
        return self.size

def get_pagination_params(
    page: int = Query(1, ge=1, description="Page number"),
    size: int = Query(50, ge=1, le=1000, description="Items per page")
) -> PaginationParams:
    """Dependency to extract page and size from query params."""
    return PaginationParams(page=page, size=size)

def calculate_pagination_meta(page: int, size: int, total: int) -> Dict[str, int]:
    """Calculate the PaginationMeta dictionary for the PaginatedResponse."""
    pages = (total + size - 1) // size if total > 0 else 1
    return {
        "page": page,
        "size": size,
        "total": total,
        "pages": pages
    }

class CursorPaginationParams(BaseModel):
    cursor: Optional[str] = None
    limit: int = 50
    
def get_cursor_pagination_params(
    cursor: Optional[str] = Query(None, description="Cursor for the next page"),
    limit: int = Query(50, ge=1, le=1000, description="Max items to return")
) -> CursorPaginationParams:
    """Dependency to extract cursor and limit for cursor-based pagination."""
    return CursorPaginationParams(cursor=cursor, limit=limit)
