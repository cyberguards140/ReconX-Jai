from pydantic import BaseModel, Field
from typing import Dict, List, Any, Optional
from datetime import datetime, timezone

class InfraEntityModel(BaseModel):
    id: str
    entity_type: str  # asn | netblock | organization | certificate
    value: str
    metadata: Dict[str, Any] = Field(default_factory=dict)
    linked_assets: List[str] = Field(default_factory=list)
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class ASNNode(InfraEntityModel):
    entity_type: str = "asn"
    name: Optional[str] = None
    country: Optional[str] = None
    netblocks: List[str] = Field(default_factory=list)

class NetblockNode(InfraEntityModel):
    entity_type: str = "netblock"
    owner_asn: Optional[str] = None

class OrganizationNode(InfraEntityModel):
    entity_type: str = "organization"
    domains: List[str] = Field(default_factory=list)
    infrastructure: List[str] = Field(default_factory=list)

class CertificateNode(InfraEntityModel):
    entity_type: str = "certificate"
    issuer: Optional[str] = None
    subject: Optional[str] = None
    domains: List[str] = Field(default_factory=list)
