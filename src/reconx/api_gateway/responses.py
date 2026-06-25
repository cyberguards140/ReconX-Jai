from typing import Generic, TypeVar, Any, Optional, List, Dict
from pydantic import BaseModel, Field
import uuid
from datetime import datetime, timezone

DataT = TypeVar("DataT")

class BaseAPIResponse(BaseModel):
    success: bool
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    request_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    version: str = "v1"

class SuccessResponse(BaseAPIResponse, Generic[DataT]):
    success: bool = True
    data: DataT
    meta: Optional[Dict[str, Any]] = None
    errors: List[Any] = Field(default_factory=list)

class ErrorDetail(BaseModel):
    field: Optional[str] = None
    message: str
    
class ErrorResponse(BaseAPIResponse):
    success: bool = False
    error_code: str
    message: str
    details: List[ErrorDetail] = Field(default_factory=list)
    data: Optional[Any] = None

class PaginationMeta(BaseModel):
    page: int
    size: int
    total: int
    pages: int

class PaginatedResponse(BaseAPIResponse, Generic[DataT]):
    success: bool = True
    data: List[DataT]
    meta: PaginationMeta
    errors: List[Any] = Field(default_factory=list)
