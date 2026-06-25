from typing import Any

from pydantic import BaseModel, Field


class ReconAsset(BaseModel):
    asset_type: str
    value: str
    sources: list[str] = Field(default_factory=list)
    confidence: float = 0.5
    related: list[dict[str, Any]] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)
