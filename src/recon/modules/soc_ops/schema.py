from pydantic import BaseModel, Field


class CaseModel(BaseModel):
    case_id: str
    title: str
    severity: str
    status: str = "New"  # New, Assigned, Investigating, Contained, Resolved, Closed, Archived
    owner: str = ""
    created_at: str
    linked_alerts: list[str] = Field(default_factory=list)
    linked_assets: list[str] = Field(default_factory=list)


class IncidentModel(BaseModel):
    incident_id: str
    case_id: str = ""
    title: str
    severity: str
    status: str = "Active"


class EvidenceModel(BaseModel):
    evidence_id: str
    evidence_type: str
    source: str
    timestamp: str
    references: list[str] = Field(default_factory=list)


class PlaybookModel(BaseModel):
    playbook_id: str
    name: str
    severity: str
    steps: list[str] = Field(default_factory=list)
