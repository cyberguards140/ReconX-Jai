from typing import Any

from pydantic import BaseModel, Field


class ExposureProfileModel(BaseModel):
    exposure_level: str = "Unknown Exposure"
    internet_visibility: bool = False
    signals: dict[str, Any] = Field(default_factory=dict)


class ReputationProfileModel(BaseModel):
    reputation: str = "neutral"
    reputation_score: int = 50
    factors: dict[str, Any] = Field(default_factory=dict)


class ExternalIntelModel(BaseModel):
    exposure: ExposureProfileModel = Field(default_factory=ExposureProfileModel)
    reputation: ReputationProfileModel = Field(default_factory=ReputationProfileModel)
    threat_indicators: list[str] = Field(default_factory=list)
    external_tags: list[str] = Field(default_factory=list)
