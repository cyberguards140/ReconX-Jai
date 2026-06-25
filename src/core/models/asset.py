from pydantic import BaseModel, Field
from typing import List, Optional, Any, Dict

class ReconAsset(BaseModel):
    asset_type: str
    value: str
    sources: List[str] = Field(default_factory=list)
    confidence: float = 0.5
    related: List[Dict[str, Any]] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)
