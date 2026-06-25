from pydantic import BaseModel, Field
from typing import List, Optional

class KnowledgeGraphEntity(BaseModel):
    """
    Base model for all entities in the Digital Twin Neo4j graph.
    """
    id: str
    tenant_id: str
    labels: List[str]

class EmployeeNode(KnowledgeGraphEntity):
    """
    Represents an employee or contractor linked to the organization.
    """
    name: str
    email: str
    department: Optional[str] = None
    is_privileged: bool = False
    labels: List[str] = ["Employee"]

class CloudResourceNode(KnowledgeGraphEntity):
    """
    Represents a managed cloud asset (S3, EC2, Lambda, IAM Role).
    """
    provider: str # e.g. "aws", "azure", "gcp"
    resource_type: str # e.g. "s3_bucket"
    arn: Optional[str] = None
    is_public: bool = False
    labels: List[str] = ["CloudResource", "Asset"]

class CertificateNode(KnowledgeGraphEntity):
    """
    Represents an SSL/TLS certificate.
    """
    common_name: str
    issuer: str
    expiration_date: str
    is_expired: bool = False
    labels: List[str] = ["Certificate"]

class ThreatActorNode(KnowledgeGraphEntity):
    """
    Represents a known APT or cybercriminal group (Phase 50/52).
    """
    name: str
    aliases: List[str] = []
    motivation: str
    labels: List[str] = ["ThreatActor"]

class KnowledgeGraphRelationship(BaseModel):
    """
    Defines complex relationships between the Digital Twin entities.
    """
    source_id: str
    target_id: str
    relation_type: str # e.g. "OWNS", "TRUSTS", "USES", "EXPOSES"
    properties: dict = Field(default_factory=dict)
