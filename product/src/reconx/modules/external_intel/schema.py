from pydantic import BaseModel, Field
from typing import Dict, List, Any

class ExposureProfileModel(BaseModel):
    exposure_level: str = "Unknown Exposure"
    internet_visibility: bool = False
    signals: Dict[str, Any] = Field(default_factory=dict)

class ReputationProfileModel(BaseModel):
    reputation: str = "neutral"
    reputation_score: int = 50
    factors: Dict[str, Any] = Field(default_factory=dict)

class ExternalIntelModel(BaseModel):
    exposure: ExposureProfileModel = Field(default_factory=ExposureProfileModel)
    reputation: ReputationProfileModel = Field(default_factory=ReputationProfileModel)
    threat_indicators: List[str] = Field(default_factory=list)
    external_tags: List[str] = Field(default_factory=list)
