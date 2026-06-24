from pydantic import BaseModel, Field
from typing import Dict, List, Any

class BusinessServiceModel(BaseModel):
    service_id: str
    service_name: str
    owner: str = ""
    criticality: str = "Medium"
    linked_assets: List[str] = Field(default_factory=list)

class RiskModel(BaseModel):
    risk_id: str
    title: str
    business_impact: str
    likelihood: str
    severity: str
    owner: str = ""
    status: str = "Open"

class ComplianceRequirementModel(BaseModel):
    requirement_id: str
    framework: str
    control: str
    status: str = "Not Evaluated"

class ProgramStatusModel(BaseModel):
    program_id: str
    name: str
    status: str
    progress: float

class KPIDashboardModel(BaseModel):
    metrics: Dict[str, float] = Field(default_factory=dict)
