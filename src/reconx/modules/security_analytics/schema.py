from pydantic import BaseModel, Field
from typing import Dict, List, Any

class NormalizedEventModel(BaseModel):
    event_id: str
    timestamp: str
    event_type: str
    source: str
    asset_id: str = ""
    severity: str = "low"
    attributes: Dict[str, Any] = Field(default_factory=dict)

class DetectionRuleModel(BaseModel):
    rule_id: str
    name: str
    severity: str = "medium"
    conditions: List[Dict[str, Any]] = Field(default_factory=list)

class AlertModel(BaseModel):
    alert_id: str
    severity: str
    title: str
    entities: List[str] = Field(default_factory=list)
    evidence: List[Dict[str, Any]] = Field(default_factory=list)

class BehaviorBaselineModel(BaseModel):
    entity: str
    baseline_score: int = 0
    anomaly_score: int = 0

class InvestigationContext(BaseModel):
    investigation_id: str
    title: str
    timeline: List[NormalizedEventModel] = Field(default_factory=list)
    related_assets: List[str] = Field(default_factory=list)
