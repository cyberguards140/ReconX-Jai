from typing import Any

from pydantic import BaseModel, Field


class IOCModel(BaseModel):
    ioc_type: str = "ip"  # ip | domain | hash | url | certificate
    value: str
    threat_level: str = "medium"  # low | medium | high | critical
    source: str
    first_seen: str
    last_seen: str


class ThreatActorModel(BaseModel):
    name: str
    aliases: list[str] = Field(default_factory=list)
    description: str = ""


class ThreatMatchModel(BaseModel):
    asset_id: str
    ioc_id: str
    campaign_id: str = ""
    match_score: int = 0


class ThreatContext(BaseModel):
    ioc_matches: list[dict[str, Any]] = Field(default_factory=list)
    actor_links: list[str] = Field(default_factory=list)
    risk_score: int = 0
    confidence: float = 0.0
