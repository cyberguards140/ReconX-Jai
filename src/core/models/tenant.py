from pydantic import BaseModel
from typing import Optional

class Organization(BaseModel):
    id: str
    name: str
    billing_tier: str = "enterprise"

class Team(BaseModel):
    id: str
    org_id: str
    name: str

class Project(BaseModel):
    id: str
    team_id: str
    name: str
    quota_limit: int = 10000

class TenantContext(BaseModel):
    """
    Passed through FastAPI Dependency Injection to ensure DB boundaries.
    """
    org_id: str
    team_id: Optional[str] = None
    project_id: Optional[str] = None
