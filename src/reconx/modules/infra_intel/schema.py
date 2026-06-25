from datetime import datetime, timezone
from typing import Any

from pydantic import BaseModel, Field


class InfraEntityModel(BaseModel):
    id: str
    entity_type: str  # asn | netblock | organization | certificate
    value: str
    metadata: dict[str, Any] = Field(default_factory=dict)
    linked_assets: list[str] = Field(default_factory=list)
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class ASNNode(InfraEntityModel):
    entity_type: str = "asn"
    name: str | None = None
    country: str | None = None
    netblocks: list[str] = Field(default_factory=list)


class NetblockNode(InfraEntityModel):
    entity_type: str = "netblock"
    owner_asn: str | None = None


class OrganizationNode(InfraEntityModel):
    entity_type: str = "organization"
    domains: list[str] = Field(default_factory=list)
    infrastructure: list[str] = Field(default_factory=list)


class CertificateNode(InfraEntityModel):
    entity_type: str = "certificate"
    issuer: str | None = None
    subject: str | None = None
    domains: list[str] = Field(default_factory=list)
