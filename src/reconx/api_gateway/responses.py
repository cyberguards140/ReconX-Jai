import uuid
from datetime import datetime, timezone
from typing import Any, Generic, TypeVar

from pydantic import BaseModel, Field

DataT = TypeVar("DataT")


class BaseAPIResponse(BaseModel):
    success: bool
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    request_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    version: str = "v1"


class SuccessResponse(BaseAPIResponse, Generic[DataT]):
    success: bool = True
    data: DataT
    meta: dict[str, Any] | None = None
    errors: list[Any] = Field(default_factory=list)


class ErrorDetail(BaseModel):
    field: str | None = None
    message: str


class ErrorResponse(BaseAPIResponse):
    success: bool = False
    error_code: str
    message: str
    details: list[ErrorDetail] = Field(default_factory=list)
    data: Any | None = None


class PaginationMeta(BaseModel):
    page: int
    size: int
    total: int
    pages: int


class PaginatedResponse(BaseAPIResponse, Generic[DataT]):
    success: bool = True
    data: list[DataT]
    meta: PaginationMeta
    errors: list[Any] = Field(default_factory=list)
