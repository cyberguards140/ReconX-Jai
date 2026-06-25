from typing import Any

from pydantic import BaseModel, Field


class NormalizedEventModel(BaseModel):
    event_id: str
    timestamp: str
    event_type: str
    source: str
    asset_id: str = ""
    severity: str = "low"
    attributes: dict[str, Any] = Field(default_factory=dict)


class DetectionRuleModel(BaseModel):
    rule_id: str
    name: str
    severity: str = "medium"
    conditions: list[dict[str, Any]] = Field(default_factory=list)


class AlertModel(BaseModel):
    alert_id: str
    severity: str
    title: str
    entities: list[str] = Field(default_factory=list)
    evidence: list[dict[str, Any]] = Field(default_factory=list)


class BehaviorBaselineModel(BaseModel):
    entity: str
    baseline_score: int = 0
    anomaly_score: int = 0


class InvestigationContext(BaseModel):
    investigation_id: str
    title: str
    timeline: list[NormalizedEventModel] = Field(default_factory=list)
    related_assets: list[str] = Field(default_factory=list)
