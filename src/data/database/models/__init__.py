import enum
from datetime import datetime, timezone
from typing import List, Optional

from sqlalchemy import JSON, Boolean, Enum, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from data.database.base import BaseModel


class SeverityEnum(str, enum.Enum):
    critical = "critical"
    high = "high"
    medium = "medium"
    low = "low"
    info = "info"


class User(BaseModel):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    role: Mapped[str] = mapped_column(String(50), default="viewer")
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    tenant_id: Mapped[str | None] = mapped_column(
        ForeignKey("tenants.id"), index=True, nullable=True
    )

    tenant: Mapped[Optional["Tenant"]] = relationship(back_populates="users")
    tenant_memberships: Mapped[list["TenantMembership"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )
    user_roles: Mapped[list["UserRole"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )
    projects: Mapped[list["Project"]] = relationship(back_populates="owner")
    refresh_tokens: Mapped[list["RefreshToken"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )
    sessions: Mapped[list["Session"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )
    audit_logs: Mapped[list["AuditLog"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )
    password_history: Mapped[list["PasswordHistory"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )


class Project(BaseModel):
    __tablename__ = "projects"

    name: Mapped[str] = mapped_column(String(100), index=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    owner_id: Mapped[str] = mapped_column(ForeignKey("users.id"), index=True)
    department_id: Mapped[str | None] = mapped_column(
        ForeignKey("departments.id"), index=True, nullable=True
    )
    organization_id: Mapped[str | None] = mapped_column(
        ForeignKey("organizations.id"), index=True, nullable=True
    )
    config: Mapped[dict | None] = mapped_column(JSON, nullable=True)

    owner: Mapped["User"] = relationship(back_populates="projects")
    department: Mapped[Optional["Department"]] = relationship()
    organization: Mapped[Optional["Organization"]] = relationship()
    targets: Mapped[list["Target"]] = relationship(
        back_populates="project", cascade="all, delete-orphan"
    )
    scans: Mapped[list["Scan"]] = relationship(
        back_populates="project", cascade="all, delete-orphan"
    )
    reports: Mapped[list["Report"]] = relationship(
        back_populates="project", cascade="all, delete-orphan"
    )
    assets: Mapped[list["Asset"]] = relationship(
        back_populates="project", cascade="all, delete-orphan"
    )


class Target(BaseModel):
    __tablename__ = "targets"

    project_id: Mapped[str] = mapped_column(ForeignKey("projects.id"), index=True)
    target: Mapped[str] = mapped_column(String(255))
    target_type: Mapped[str] = mapped_column(String(50))
    status: Mapped[str] = mapped_column(String(50), default="active")

    project: Mapped["Project"] = relationship(back_populates="targets")
    scans: Mapped[list["Scan"]] = relationship(
        back_populates="target", cascade="all, delete-orphan"
    )
    plugin_executions: Mapped[list["PluginExecution"]] = relationship(
        back_populates="target", cascade="all, delete-orphan"
    )


class Scan(BaseModel):
    __tablename__ = "scans"

    project_id: Mapped[str] = mapped_column(ForeignKey("projects.id"), index=True)
    target_id: Mapped[str] = mapped_column(ForeignKey("targets.id"), index=True)
    scan_type: Mapped[str] = mapped_column(String(50))
    status: Mapped[str] = mapped_column(String(50), default="pending")
    started_at: Mapped[datetime | None] = mapped_column(nullable=True)
    completed_at: Mapped[datetime | None] = mapped_column(nullable=True)

    project: Mapped["Project"] = relationship(back_populates="scans")
    target: Mapped["Target"] = relationship(back_populates="scans")
    findings: Mapped[list["Finding"]] = relationship(
        back_populates="scan", cascade="all, delete-orphan"
    )


class Finding(BaseModel):
    __tablename__ = "findings"

    scan_id: Mapped[str] = mapped_column(ForeignKey("scans.id"), index=True)
    asset_id: Mapped[str | None] = mapped_column(ForeignKey("assets.id"), index=True, nullable=True)
    severity: Mapped[SeverityEnum] = mapped_column(Enum(SeverityEnum), index=True)
    title: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(Text)
    evidence: Mapped[str | None] = mapped_column(Text, nullable=True)
    source_tool: Mapped[str | None] = mapped_column(String(100), nullable=True)

    scan: Mapped["Scan"] = relationship(back_populates="findings")
    asset: Mapped[Optional["Asset"]] = relationship(back_populates="findings")


class Asset(BaseModel):
    __tablename__ = "assets"

    project_id: Mapped[str] = mapped_column(ForeignKey("projects.id"), index=True)
    asset_type: Mapped[str] = mapped_column(String(50))
    value: Mapped[str] = mapped_column(String(255))
    hostname: Mapped[str | None] = mapped_column(String(255), nullable=True)
    mac_address: Mapped[str | None] = mapped_column(String(50), nullable=True)
    registrar: Mapped[str | None] = mapped_column(String(255), nullable=True)
    created_at: Mapped[str | None] = mapped_column(String(50), nullable=True)
    expires_at: Mapped[str | None] = mapped_column(String(50), nullable=True)
    is_resolved: Mapped[bool | None] = mapped_column(Boolean, default=False, nullable=True)
    organization: Mapped[str | None] = mapped_column(String(255), nullable=True)
    owner_id: Mapped[str | None] = mapped_column(ForeignKey("users.id"), index=True, nullable=True)
    tags: Mapped[list | None] = mapped_column(JSON, nullable=True)
    lifecycle_status: Mapped[str] = mapped_column(String(50), default="active")
    source: Mapped[str | None] = mapped_column(String(255), nullable=True)
    sources: Mapped[list | None] = mapped_column(JSON, nullable=True)
    confidence: Mapped[float] = mapped_column(Float, default=0.0)
    metadata_json: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    external_intel_json: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    visual_intel_json: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    threat_intel_json: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    cloud_intel_json: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    security_analytics_json: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    soc_ops_json: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    executive_intel_json: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    timestamp: Mapped[datetime | None] = mapped_column(nullable=True)

    project: Mapped["Project"] = relationship(back_populates="assets")
    owner: Mapped[Optional["User"]] = relationship()
    findings: Mapped[list["Finding"]] = relationship(
        back_populates="asset", cascade="all, delete-orphan"
    )
    ports: Mapped[list["Port"]] = relationship(back_populates="asset", cascade="all, delete-orphan")
    services: Mapped[list["Service"]] = relationship(
        back_populates="asset", cascade="all, delete-orphan"
    )
    technologies: Mapped[list["Technology"]] = relationship(
        back_populates="asset", cascade="all, delete-orphan"
    )
    screenshots: Mapped[list["Screenshot"]] = relationship(
        back_populates="asset", cascade="all, delete-orphan"
    )
    dns_records: Mapped[list["DNSRecord"]] = relationship(
        back_populates="asset", cascade="all, delete-orphan"
    )


class Port(BaseModel):
    __tablename__ = "ports"

    asset_id: Mapped[str] = mapped_column(ForeignKey("assets.id"), index=True)
    port: Mapped[int] = mapped_column()
    protocol: Mapped[str] = mapped_column(String(20))
    state: Mapped[str] = mapped_column(String(50))

    asset: Mapped["Asset"] = relationship(back_populates="ports")


class Service(BaseModel):
    __tablename__ = "services"

    asset_id: Mapped[str] = mapped_column(ForeignKey("assets.id"), index=True)
    port: Mapped[int] = mapped_column()
    service: Mapped[str] = mapped_column(String(100))
    product: Mapped[str | None] = mapped_column(String(255), nullable=True)
    version: Mapped[str | None] = mapped_column(String(100), nullable=True)

    asset: Mapped["Asset"] = relationship(back_populates="services")


class Technology(BaseModel):
    __tablename__ = "technologies"

    asset_id: Mapped[str] = mapped_column(ForeignKey("assets.id"), index=True)
    service_id: Mapped[str | None] = mapped_column(
        ForeignKey("services.id"), index=True, nullable=True
    )
    technology: Mapped[str] = mapped_column(String(255))
    version: Mapped[str | None] = mapped_column(String(100), nullable=True)

    asset: Mapped["Asset"] = relationship(back_populates="technologies")
    service: Mapped[Optional["Service"]] = relationship()


class CMS(BaseModel):
    __tablename__ = "cms"

    asset_id: Mapped[str] = mapped_column(ForeignKey("assets.id"), index=True)
    service_id: Mapped[str | None] = mapped_column(
        ForeignKey("services.id"), index=True, nullable=True
    )
    cms: Mapped[str] = mapped_column(String(255))
    version: Mapped[str | None] = mapped_column(String(100), nullable=True)


class Framework(BaseModel):
    __tablename__ = "frameworks"

    asset_id: Mapped[str] = mapped_column(ForeignKey("assets.id"), index=True)
    service_id: Mapped[str | None] = mapped_column(
        ForeignKey("services.id"), index=True, nullable=True
    )
    framework: Mapped[str] = mapped_column(String(255))
    version: Mapped[str | None] = mapped_column(String(100), nullable=True)


class WAF(BaseModel):
    __tablename__ = "wafs"

    asset_id: Mapped[str] = mapped_column(ForeignKey("assets.id"), index=True)
    service_id: Mapped[str | None] = mapped_column(
        ForeignKey("services.id"), index=True, nullable=True
    )
    vendor: Mapped[str] = mapped_column(String(255))
    detected: Mapped[bool] = mapped_column(Boolean, default=True)


class HTTPHeader(BaseModel):
    __tablename__ = "http_headers"

    asset_id: Mapped[str] = mapped_column(ForeignKey("assets.id"), index=True)
    service_id: Mapped[str | None] = mapped_column(
        ForeignKey("services.id"), index=True, nullable=True
    )
    name: Mapped[str] = mapped_column(String(255))
    value: Mapped[str] = mapped_column(Text)
    is_security: Mapped[bool] = mapped_column(Boolean, default=False)


class Certificate(BaseModel):
    __tablename__ = "certificates"

    asset_id: Mapped[str] = mapped_column(ForeignKey("assets.id"), index=True)
    service_id: Mapped[str | None] = mapped_column(
        ForeignKey("services.id"), index=True, nullable=True
    )
    issuer: Mapped[str] = mapped_column(String(255))
    subject: Mapped[str] = mapped_column(String(255))
    valid_from: Mapped[str | None] = mapped_column(String(50), nullable=True)
    valid_until: Mapped[str | None] = mapped_column(String(50), nullable=True)
    san_entries: Mapped[list | None] = mapped_column(JSON, nullable=True)


class TLSConfiguration(BaseModel):
    __tablename__ = "tls_configurations"

    asset_id: Mapped[str] = mapped_column(ForeignKey("assets.id"), index=True)
    service_id: Mapped[str | None] = mapped_column(
        ForeignKey("services.id"), index=True, nullable=True
    )
    protocol: Mapped[str] = mapped_column(String(50))
    enabled: Mapped[bool] = mapped_column(Boolean, default=True)


class CipherSuite(BaseModel):
    __tablename__ = "cipher_suites"

    asset_id: Mapped[str] = mapped_column(ForeignKey("assets.id"), index=True)
    service_id: Mapped[str | None] = mapped_column(
        ForeignKey("services.id"), index=True, nullable=True
    )
    protocol: Mapped[str] = mapped_column(String(50))
    cipher: Mapped[str] = mapped_column(String(255))
    strength: Mapped[str] = mapped_column(String(50))


class SMBHost(BaseModel):
    __tablename__ = "smb_hosts"

    asset_id: Mapped[str] = mapped_column(ForeignKey("assets.id"), index=True)
    hostname: Mapped[str] = mapped_column(String(255))
    domain: Mapped[str | None] = mapped_column(String(255), nullable=True)
    os: Mapped[str | None] = mapped_column(String(255), nullable=True)
    sources: Mapped[list | None] = mapped_column(JSON, nullable=True)


class SMBShare(BaseModel):
    __tablename__ = "smb_shares"

    asset_id: Mapped[str] = mapped_column(ForeignKey("assets.id"), index=True)
    share_name: Mapped[str] = mapped_column(String(255))
    comment: Mapped[str | None] = mapped_column(Text, nullable=True)
    type: Mapped[str | None] = mapped_column(String(100), nullable=True)
    sources: Mapped[list | None] = mapped_column(JSON, nullable=True)


class SMBUser(BaseModel):
    __tablename__ = "smb_users"

    asset_id: Mapped[str] = mapped_column(ForeignKey("assets.id"), index=True)
    username: Mapped[str] = mapped_column(String(255))
    sources: Mapped[list | None] = mapped_column(JSON, nullable=True)


class SMBGroup(BaseModel):
    __tablename__ = "smb_groups"

    asset_id: Mapped[str] = mapped_column(ForeignKey("assets.id"), index=True)
    group_name: Mapped[str] = mapped_column(String(255))
    sources: Mapped[list | None] = mapped_column(JSON, nullable=True)


class SMBPasswordPolicy(BaseModel):
    __tablename__ = "smb_password_policies"

    asset_id: Mapped[str] = mapped_column(ForeignKey("assets.id"), index=True)
    minimum_length: Mapped[int | None] = mapped_column(Integer, nullable=True)
    lockout_enabled: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    sources: Mapped[list | None] = mapped_column(JSON, nullable=True)


class SMBConfiguration(BaseModel):
    __tablename__ = "smb_configurations"

    asset_id: Mapped[str] = mapped_column(ForeignKey("assets.id"), index=True)
    signing_required: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    smbv1_enabled: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    sources: Mapped[list | None] = mapped_column(JSON, nullable=True)


class ADDomain(BaseModel):
    __tablename__ = "ad_domains"

    domain_name: Mapped[str] = mapped_column(String(255), unique=True)
    forest: Mapped[str | None] = mapped_column(String(255), nullable=True)
    sources: Mapped[list | None] = mapped_column(JSON, nullable=True)


class ADUser(BaseModel):
    __tablename__ = "ad_users"

    domain: Mapped[str] = mapped_column(String(255))
    username: Mapped[str] = mapped_column(String(255))
    display_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    sources: Mapped[list | None] = mapped_column(JSON, nullable=True)


class ADGroup(BaseModel):
    __tablename__ = "ad_groups"

    domain: Mapped[str] = mapped_column(String(255))
    group_name: Mapped[str] = mapped_column(String(255))
    members_count: Mapped[int | None] = mapped_column(Integer, nullable=True)
    sources: Mapped[list | None] = mapped_column(JSON, nullable=True)


class ADComputer(BaseModel):
    __tablename__ = "ad_computers"

    domain: Mapped[str] = mapped_column(String(255))
    hostname: Mapped[str] = mapped_column(String(255))
    os: Mapped[str | None] = mapped_column(String(255), nullable=True)
    asset_id: Mapped[str | None] = mapped_column(ForeignKey("assets.id"), index=True, nullable=True)
    sources: Mapped[list | None] = mapped_column(JSON, nullable=True)


class ADOrganizationalUnit(BaseModel):
    __tablename__ = "ad_organizational_units"

    domain: Mapped[str] = mapped_column(String(255))
    ou_name: Mapped[str] = mapped_column(String(255))
    sources: Mapped[list | None] = mapped_column(JSON, nullable=True)


class ADTrustRelationship(BaseModel):
    __tablename__ = "ad_trust_relationships"

    source_domain: Mapped[str] = mapped_column(String(255))
    target_domain: Mapped[str] = mapped_column(String(255))
    trust_type: Mapped[str | None] = mapped_column(String(100), nullable=True)
    sources: Mapped[list | None] = mapped_column(JSON, nullable=True)


class OSINTOrganization(BaseModel):
    __tablename__ = "osint_organizations"

    organization: Mapped[str] = mapped_column(String(255), unique=True)
    sources: Mapped[list | None] = mapped_column(JSON, nullable=True)


class OSINTEmail(BaseModel):
    __tablename__ = "osint_emails"

    email: Mapped[str] = mapped_column(String(255), unique=True)
    sources: Mapped[list | None] = mapped_column(JSON, nullable=True)


class OSINTUsername(BaseModel):
    __tablename__ = "osint_usernames"

    username: Mapped[str] = mapped_column(String(255), unique=True)
    sources: Mapped[list | None] = mapped_column(JSON, nullable=True)


class OSINTProfile(BaseModel):
    __tablename__ = "osint_profiles"

    username: Mapped[str] = mapped_column(String(255))
    platform: Mapped[str] = mapped_column(String(100))
    profile_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    sources: Mapped[list | None] = mapped_column(JSON, nullable=True)


class OSINTRelationship(BaseModel):
    __tablename__ = "osint_relationships"

    source_entity: Mapped[str] = mapped_column(String(255))
    target_entity: Mapped[str] = mapped_column(String(255))
    relationship_type: Mapped[str] = mapped_column(String(100))
    sources: Mapped[list | None] = mapped_column(JSON, nullable=True)


class TrafficFlow(BaseModel):
    __tablename__ = "traffic_flows"

    src_ip: Mapped[str] = mapped_column(String(255))
    dst_ip: Mapped[str] = mapped_column(String(255))
    protocol: Mapped[str] = mapped_column(String(100))
    sources: Mapped[list | None] = mapped_column(JSON, nullable=True)


class TrafficProtocol(BaseModel):
    __tablename__ = "traffic_protocols"

    protocol: Mapped[str] = mapped_column(String(100), unique=True)
    sources: Mapped[list | None] = mapped_column(JSON, nullable=True)


class TrafficCommunication(BaseModel):
    __tablename__ = "traffic_communications"

    host_a: Mapped[str] = mapped_column(String(255))
    host_b: Mapped[str] = mapped_column(String(255))
    protocol: Mapped[str] = mapped_column(String(100))
    sources: Mapped[list | None] = mapped_column(JSON, nullable=True)


class TrafficDNSQuery(BaseModel):
    __tablename__ = "traffic_dns_queries"

    domain: Mapped[str] = mapped_column(String(255))
    query_type: Mapped[str | None] = mapped_column(String(50), nullable=True)
    sources: Mapped[list | None] = mapped_column(JSON, nullable=True)


class TrafficHTTPMetadata(BaseModel):
    __tablename__ = "traffic_http_metadata"

    host: Mapped[str] = mapped_column(String(255))
    method: Mapped[str] = mapped_column(String(50))
    uri: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    sources: Mapped[list | None] = mapped_column(JSON, nullable=True)


class TrafficTLSMetadata(BaseModel):
    __tablename__ = "traffic_tls_metadata"

    sni: Mapped[str] = mapped_column(String(255))
    tls_version: Mapped[str | None] = mapped_column(String(50), nullable=True)
    sources: Mapped[list | None] = mapped_column(JSON, nullable=True)


class TrafficStatistic(BaseModel):
    __tablename__ = "traffic_statistics"

    stat_name: Mapped[str] = mapped_column(String(100))
    stat_value: Mapped[str] = mapped_column(String(500))
    sources: Mapped[list | None] = mapped_column(JSON, nullable=True)


class CloudAccount(BaseModel):
    __tablename__ = "cloud_accounts"

    provider: Mapped[str] = mapped_column(String(100))
    account_id: Mapped[str] = mapped_column(String(255), unique=True)
    sources: Mapped[list | None] = mapped_column(JSON, nullable=True)


class CloudResource(BaseModel):
    __tablename__ = "cloud_resources"

    account_id: Mapped[str] = mapped_column(String(255))
    resource_type: Mapped[str] = mapped_column(String(100))
    resource_id: Mapped[str] = mapped_column(String(500))
    sources: Mapped[list | None] = mapped_column(JSON, nullable=True)


class CloudKubernetesCluster(BaseModel):
    __tablename__ = "cloud_kubernetes_clusters"

    cluster_name: Mapped[str] = mapped_column(String(255), unique=True)
    sources: Mapped[list | None] = mapped_column(JSON, nullable=True)


class CloudNamespace(BaseModel):
    __tablename__ = "cloud_namespaces"

    cluster_name: Mapped[str] = mapped_column(String(255))
    namespace: Mapped[str] = mapped_column(String(255))
    sources: Mapped[list | None] = mapped_column(JSON, nullable=True)


class CloudPod(BaseModel):
    __tablename__ = "cloud_pods"

    namespace: Mapped[str] = mapped_column(String(255))
    pod_name: Mapped[str] = mapped_column(String(255))
    sources: Mapped[list | None] = mapped_column(JSON, nullable=True)


class CloudDeployment(BaseModel):
    __tablename__ = "cloud_deployments"

    namespace: Mapped[str] = mapped_column(String(255))
    deployment_name: Mapped[str] = mapped_column(String(255))
    sources: Mapped[list | None] = mapped_column(JSON, nullable=True)


class CloudContainerImage(BaseModel):
    __tablename__ = "cloud_container_images"

    image: Mapped[str] = mapped_column(String(500))
    tag: Mapped[str | None] = mapped_column(String(100), nullable=True)
    sources: Mapped[list | None] = mapped_column(JSON, nullable=True)


class CloudContainerFinding(BaseModel):
    __tablename__ = "cloud_container_findings"

    image: Mapped[str] = mapped_column(String(500))
    vulnerability_id: Mapped[str] = mapped_column(String(100))
    severity: Mapped[str | None] = mapped_column(String(50), nullable=True)
    sources: Mapped[list | None] = mapped_column(JSON, nullable=True)


class VulnCVE(BaseModel):
    __tablename__ = "vuln_cves"

    cve_id: Mapped[str] = mapped_column(String(100), unique=True)
    title: Mapped[str | None] = mapped_column(String(500), nullable=True)
    cvss_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    severity: Mapped[str | None] = mapped_column(String(50), nullable=True)
    sources: Mapped[list | None] = mapped_column(JSON, nullable=True)


class VulnCPE(BaseModel):
    __tablename__ = "vuln_cpes"

    cpe_string: Mapped[str] = mapped_column(String(500), unique=True)
    product: Mapped[str | None] = mapped_column(String(255), nullable=True)
    version: Mapped[str | None] = mapped_column(String(255), nullable=True)
    sources: Mapped[list | None] = mapped_column(JSON, nullable=True)


class VulnRecord(BaseModel):
    __tablename__ = "vuln_records"

    asset_id: Mapped[str] = mapped_column(String(255))
    cve_id: Mapped[str | None] = mapped_column(String(100), nullable=True)
    title: Mapped[str] = mapped_column(String(500))
    severity: Mapped[str | None] = mapped_column(String(50), nullable=True)
    sources: Mapped[list | None] = mapped_column(JSON, nullable=True)


class VulnRiskProfile(BaseModel):
    __tablename__ = "vuln_risk_profiles"

    asset_id: Mapped[str] = mapped_column(String(255), unique=True)
    risk_score: Mapped[float] = mapped_column(Float, default=0.0)
    critical_count: Mapped[int] = mapped_column(Integer, default=0)
    high_count: Mapped[int] = mapped_column(Integer, default=0)
    medium_count: Mapped[int] = mapped_column(Integer, default=0)
    low_count: Mapped[int] = mapped_column(Integer, default=0)
    sources: Mapped[list | None] = mapped_column(JSON, nullable=True)


class VulnEvidence(BaseModel):
    __tablename__ = "vuln_evidence"

    finding_id: Mapped[str] = mapped_column(String(255))
    evidence_data: Mapped[str] = mapped_column(Text)
    sources: Mapped[list | None] = mapped_column(JSON, nullable=True)


class VulnReference(BaseModel):
    __tablename__ = "vuln_references"

    entity_id: Mapped[str] = mapped_column(String(255))  # Could be a CVE or a Finding
    url: Mapped[str] = mapped_column(String(1000))
    sources: Mapped[list | None] = mapped_column(JSON, nullable=True)


class ReportRecord(BaseModel):
    __tablename__ = "report_records"

    report_id: Mapped[str] = mapped_column(String(255), unique=True)
    report_type: Mapped[str] = mapped_column(String(100))  # e.g. Executive, Technical
    title: Mapped[str] = mapped_column(String(500))
    generated_at: Mapped[str | None] = mapped_column(String(100), nullable=True)
    metadata_json: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    sources: Mapped[list | None] = mapped_column(JSON, nullable=True)


class ReportEvidence(BaseModel):
    __tablename__ = "report_evidence"

    finding_id: Mapped[str] = mapped_column(String(255))
    evidence_path: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    raw_content: Mapped[str | None] = mapped_column(Text, nullable=True)
    sources: Mapped[list | None] = mapped_column(JSON, nullable=True)


class ReportExport(BaseModel):
    __tablename__ = "report_exports"

    report_id: Mapped[str] = mapped_column(String(255))
    export_format: Mapped[str] = mapped_column(String(50))  # e.g. PDF, JSON
    export_path: Mapped[str] = mapped_column(String(1000))
    sources: Mapped[list | None] = mapped_column(JSON, nullable=True)


class ReportScanHistory(BaseModel):
    __tablename__ = "report_scan_history"

    scan_id: Mapped[str] = mapped_column(String(255), unique=True)
    scan_name: Mapped[str] = mapped_column(String(500))
    timestamp: Mapped[str] = mapped_column(String(100))
    targets: Mapped[list | None] = mapped_column(JSON, nullable=True)
    sources: Mapped[list | None] = mapped_column(JSON, nullable=True)


class ReportTemplate(BaseModel):
    __tablename__ = "report_templates"

    template_name: Mapped[str] = mapped_column(String(255), unique=True)
    template_path: Mapped[str] = mapped_column(String(1000))
    sources: Mapped[list | None] = mapped_column(JSON, nullable=True)


class GraphNode(BaseModel):
    __tablename__ = "graph_nodes"

    node_id: Mapped[str] = mapped_column(String(255), unique=True)
    node_type: Mapped[str] = mapped_column(String(100))  # e.g. Domain, User, Vulnerability
    label: Mapped[str] = mapped_column(String(500))
    properties: Mapped[dict | None] = mapped_column(JSON, nullable=True)


class GraphEdge(BaseModel):
    __tablename__ = "graph_edges"

    edge_id: Mapped[str] = mapped_column(String(255), unique=True)
    source_node_id: Mapped[str] = mapped_column(String(255))
    target_node_id: Mapped[str] = mapped_column(String(255))
    edge_type: Mapped[str] = mapped_column(String(100))  # e.g. RESOLVES_TO, MEMBER_OF
    properties: Mapped[dict | None] = mapped_column(JSON, nullable=True)


class GraphSnapshot(BaseModel):
    __tablename__ = "graph_snapshots"

    snapshot_id: Mapped[str] = mapped_column(String(255), unique=True)
    timestamp: Mapped[str] = mapped_column(String(100))
    total_nodes: Mapped[int] = mapped_column(Integer, default=0)
    total_edges: Mapped[int] = mapped_column(Integer, default=0)
    data: Mapped[dict | None] = mapped_column(JSON, nullable=True)


class AnalyticsRiskScore(BaseModel):
    __tablename__ = "analytics_risk_scores"

    asset_id: Mapped[str] = mapped_column(String(255), unique=True)
    risk_score: Mapped[float] = mapped_column(Float, default=0.0)
    criticality: Mapped[str] = mapped_column(String(50))  # e.g. Low, Medium, High, Critical
    exposure: Mapped[str] = mapped_column(String(50))  # e.g. Internal, External, Cloud
    factors: Mapped[list | None] = mapped_column(JSON, nullable=True)


class AnalyticsAssetProfile(BaseModel):
    __tablename__ = "analytics_asset_profiles"

    asset_id: Mapped[str] = mapped_column(String(255), unique=True)
    ip: Mapped[str | None] = mapped_column(String(100), nullable=True)
    service_count: Mapped[int] = mapped_column(Integer, default=0)
    finding_count: Mapped[int] = mapped_column(Integer, default=0)
    risk_score: Mapped[float] = mapped_column(Float, default=0.0)
    metadata_json: Mapped[dict | None] = mapped_column(JSON, nullable=True)


class AnalyticsRecommendation(BaseModel):
    __tablename__ = "analytics_recommendations"

    recommendation_id: Mapped[str] = mapped_column(String(255), unique=True)
    title: Mapped[str] = mapped_column(String(500))
    description: Mapped[str] = mapped_column(Text)
    impact: Mapped[str] = mapped_column(String(50))  # e.g. Quick Win, High Impact
    affected_assets: Mapped[int] = mapped_column(Integer, default=0)


class AnalyticsTrendData(BaseModel):
    __tablename__ = "analytics_trend_data"

    trend_id: Mapped[str] = mapped_column(String(255), unique=True)
    timestamp: Mapped[str] = mapped_column(String(100))
    metric_name: Mapped[str] = mapped_column(String(100))
    value: Mapped[float] = mapped_column(Float)


class AnalyticsPriority(BaseModel):
    __tablename__ = "analytics_priorities"

    asset_id: Mapped[str] = mapped_column(String(255), unique=True)
    priority_rank: Mapped[int] = mapped_column(Integer)
    reason: Mapped[str] = mapped_column(Text)


class AutomationJob(BaseModel):
    __tablename__ = "automation_jobs"

    job_id: Mapped[str] = mapped_column(String(255), unique=True)
    job_type: Mapped[str] = mapped_column(String(100))  # e.g. QuickRecon, Standard
    status: Mapped[str] = mapped_column(String(50))  # e.g. Pending, Running, Completed, Failed
    created_at: Mapped[str] = mapped_column(String(100))
    completed_at: Mapped[str | None] = mapped_column(String(100), nullable=True)
    result_metadata: Mapped[dict | None] = mapped_column(JSON, nullable=True)


class AutomationSchedule(BaseModel):
    __tablename__ = "automation_schedules"

    schedule_id: Mapped[str] = mapped_column(String(255), unique=True)
    job_type: Mapped[str] = mapped_column(String(100))
    interval: Mapped[str] = mapped_column(String(50))  # e.g. Hourly, Daily, Weekly, Custom Cron
    last_run: Mapped[str | None] = mapped_column(String(100), nullable=True)
    next_run: Mapped[str | None] = mapped_column(String(100), nullable=True)


class AutomationAlert(BaseModel):
    __tablename__ = "automation_alerts"

    alert_id: Mapped[str] = mapped_column(String(255), unique=True)
    severity: Mapped[str] = mapped_column(String(50))  # Critical, High, Medium, Low, Informational
    message: Mapped[str] = mapped_column(String(1000))
    source: Mapped[str] = mapped_column(String(100))  # e.g. Findings, Risk Changes, Asset Changes
    timestamp: Mapped[str] = mapped_column(String(100))


class AutomationWorkflowRun(BaseModel):
    __tablename__ = "automation_workflow_runs"

    run_id: Mapped[str] = mapped_column(String(255), unique=True)
    workflow_name: Mapped[str] = mapped_column(String(255))
    status: Mapped[str] = mapped_column(String(50))
    tasks_completed: Mapped[int] = mapped_column(Integer, default=0)
    tasks_total: Mapped[int] = mapped_column(Integer, default=0)


class AutomationChangeEvent(BaseModel):
    __tablename__ = "automation_change_events"

    event_id: Mapped[str] = mapped_column(String(255), unique=True)
    change_type: Mapped[str] = mapped_column(String(100))  # e.g. Added, Removed, Modified
    entity_type: Mapped[str] = mapped_column(String(100))  # e.g. Asset, Finding, Technology
    entity_id: Mapped[str] = mapped_column(String(255))
    metadata_json: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    timestamp: Mapped[str] = mapped_column(String(100))


class EnterpriseTenant(BaseModel):
    __tablename__ = "enterprise_tenants"
    tenant_id: Mapped[str] = mapped_column(String(255), unique=True)
    name: Mapped[str] = mapped_column(String(255))


class EnterpriseProject(BaseModel):
    __tablename__ = "enterprise_projects"
    project_id: Mapped[str] = mapped_column(String(255), unique=True)
    tenant_id: Mapped[str] = mapped_column(String(255))
    name: Mapped[str] = mapped_column(String(255))


class EnterpriseUser(BaseModel):
    __tablename__ = "enterprise_users"
    user_id: Mapped[str] = mapped_column(String(255), unique=True)
    tenant_id: Mapped[str] = mapped_column(String(255))
    username: Mapped[str] = mapped_column(String(255))
    email: Mapped[str] = mapped_column(String(255))


class EnterpriseRole(BaseModel):
    __tablename__ = "enterprise_roles"
    role_id: Mapped[str] = mapped_column(String(255), unique=True)
    name: Mapped[str] = mapped_column(String(100))  # e.g. Viewer, Analyst, Operator, Admin


class EnterprisePermission(BaseModel):
    __tablename__ = "enterprise_permissions"
    permission_id: Mapped[str] = mapped_column(String(255), unique=True)
    role_id: Mapped[str] = mapped_column(String(255))
    action: Mapped[str] = mapped_column(String(255))  # e.g. View_Assets, Run_Jobs


class EnterpriseAuditLog(BaseModel):
    __tablename__ = "enterprise_audit_logs"
    log_id: Mapped[str] = mapped_column(String(255), unique=True)
    tenant_id: Mapped[str] = mapped_column(String(255))
    user_id: Mapped[str] = mapped_column(String(255))
    action: Mapped[str] = mapped_column(String(500))
    timestamp: Mapped[str] = mapped_column(String(100))


class EnterpriseAPIKey(BaseModel):
    __tablename__ = "enterprise_api_keys"
    key_id: Mapped[str] = mapped_column(String(255), unique=True)
    user_id: Mapped[str] = mapped_column(String(255))
    hashed_token: Mapped[str] = mapped_column(String(500))
    status: Mapped[str] = mapped_column(String(50))  # Active, Revoked


class EnterpriseTeam(BaseModel):
    __tablename__ = "enterprise_teams"
    team_id: Mapped[str] = mapped_column(String(255), unique=True)
    tenant_id: Mapped[str] = mapped_column(String(255))
    name: Mapped[str] = mapped_column(String(255))


class EnterpriseOwnership(BaseModel):
    __tablename__ = "enterprise_ownership"
    ownership_id: Mapped[str] = mapped_column(String(255), unique=True)
    entity_id: Mapped[str] = mapped_column(String(255))  # e.g. asset_id
    owner_type: Mapped[str] = mapped_column(String(100))  # Team or User
    owner_id: Mapped[str] = mapped_column(String(255))


class ContentItem(BaseModel):
    __tablename__ = "content_items"

    asset_id: Mapped[str] = mapped_column(ForeignKey("assets.id"), index=True)
    service_id: Mapped[str | None] = mapped_column(
        ForeignKey("services.id"), index=True, nullable=True
    )
    technology_id: Mapped[str | None] = mapped_column(
        ForeignKey("technologies.id"), index=True, nullable=True
    )
    url: Mapped[str] = mapped_column(String(500))
    path: Mapped[str] = mapped_column(String(500))
    status_code: Mapped[int] = mapped_column(Integer, default=200)
    content_length: Mapped[int | None] = mapped_column(Integer, nullable=True)
    content_type: Mapped[str | None] = mapped_column(String(100), nullable=True)
    sources: Mapped[list | None] = mapped_column(JSON, nullable=True)


class Endpoint(BaseModel):
    __tablename__ = "endpoints"

    asset_id: Mapped[str] = mapped_column(ForeignKey("assets.id"), index=True)
    service_id: Mapped[str | None] = mapped_column(
        ForeignKey("services.id"), index=True, nullable=True
    )
    method: Mapped[str] = mapped_column(String(20))
    path: Mapped[str] = mapped_column(String(500))
    sources: Mapped[list | None] = mapped_column(JSON, nullable=True)


class VirtualHost(BaseModel):
    __tablename__ = "virtual_hosts"

    asset_id: Mapped[str] = mapped_column(ForeignKey("assets.id"), index=True)
    service_id: Mapped[str | None] = mapped_column(
        ForeignKey("services.id"), index=True, nullable=True
    )
    vhost: Mapped[str] = mapped_column(String(255))
    sources: Mapped[list | None] = mapped_column(JSON, nullable=True)


class Screenshot(BaseModel):
    __tablename__ = "screenshots"

    asset_id: Mapped[str] = mapped_column(ForeignKey("assets.id"), index=True)
    path: Mapped[str] = mapped_column(String(500))
    title: Mapped[str | None] = mapped_column(String(255), nullable=True)

    asset: Mapped["Asset"] = relationship(back_populates="screenshots")


class Route(BaseModel):
    __tablename__ = "routes"

    asset_id: Mapped[str] = mapped_column(ForeignKey("assets.id"), index=True)
    hop_count: Mapped[int] = mapped_column()
    node_ip: Mapped[str] = mapped_column(String(50))
    latency: Mapped[float | None] = mapped_column(nullable=True)

    asset: Mapped["Asset"] = relationship("Asset")


class DNSRecord(BaseModel):
    __tablename__ = "dns_records"

    asset_id: Mapped[str] = mapped_column(ForeignKey("assets.id"), index=True)
    record_type: Mapped[str] = mapped_column(String(20))
    value: Mapped[str] = mapped_column(Text)

    asset: Mapped["Asset"] = relationship(back_populates="dns_records")


class Report(BaseModel):
    __tablename__ = "reports"

    project_id: Mapped[str] = mapped_column(ForeignKey("projects.id"), index=True)
    report_type: Mapped[str] = mapped_column(String(50))
    file_path: Mapped[str] = mapped_column(String(500))
    generated_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc))

    project: Mapped["Project"] = relationship(back_populates="reports")


class PluginExecution(BaseModel):
    __tablename__ = "plugin_executions"

    plugin_name: Mapped[str] = mapped_column(String(100), index=True)
    target_id: Mapped[str] = mapped_column(ForeignKey("targets.id"), index=True)
    status: Mapped[str] = mapped_column(String(50), default="running")
    started_at: Mapped[datetime | None] = mapped_column(nullable=True)
    finished_at: Mapped[datetime | None] = mapped_column(nullable=True)
    output: Mapped[str | None] = mapped_column(Text, nullable=True)

    target: Mapped["Target"] = relationship(back_populates="plugin_executions")


class RefreshToken(BaseModel):
    __tablename__ = "refresh_tokens"

    token_id: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"), index=True)
    tenant_id: Mapped[str | None] = mapped_column(
        ForeignKey("tenants.id"), index=True, nullable=True
    )
    issued_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc))
    expires_at: Mapped[datetime] = mapped_column()
    revoked: Mapped[bool] = mapped_column(Boolean, default=False)

    user: Mapped["User"] = relationship(back_populates="refresh_tokens")


class Session(BaseModel):
    __tablename__ = "sessions"

    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"), index=True)
    tenant_id: Mapped[str | None] = mapped_column(
        ForeignKey("tenants.id"), index=True, nullable=True
    )
    session_id: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    ip_address: Mapped[str | None] = mapped_column(String(50), nullable=True)
    user_agent: Mapped[str | None] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc))
    last_seen: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc))
    expires_at: Mapped[datetime | None] = mapped_column(nullable=True)
    login_time: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc))
    logout_time: Mapped[datetime | None] = mapped_column(nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    user: Mapped["User"] = relationship(back_populates="sessions")


class AuditLog(BaseModel):
    __tablename__ = "audit_logs"

    user_id: Mapped[str | None] = mapped_column(ForeignKey("users.id"), index=True, nullable=True)
    actor: Mapped[str | None] = mapped_column(String(255), nullable=True)
    tenant_id: Mapped[str | None] = mapped_column(
        ForeignKey("tenants.id"), index=True, nullable=True
    )
    action: Mapped[str] = mapped_column(String(100), index=True)
    resource_type: Mapped[str | None] = mapped_column(String(100), nullable=True)
    resource_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    resource: Mapped[str | None] = mapped_column(String(255), nullable=True)
    status: Mapped[str | None] = mapped_column(String(50), nullable=True)
    request_path: Mapped[str | None] = mapped_column(String(500), nullable=True)
    method: Mapped[str | None] = mapped_column(String(20), nullable=True)
    response_status: Mapped[int | None] = mapped_column(Integer, nullable=True)
    execution_time: Mapped[float | None] = mapped_column(Float, nullable=True)
    timestamp: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc))
    ip_address: Mapped[str | None] = mapped_column(String(50), nullable=True)
    user_agent: Mapped[str | None] = mapped_column(String(500), nullable=True)

    user: Mapped[Optional["User"]] = relationship(back_populates="audit_logs")


class PasswordHistory(BaseModel):
    __tablename__ = "password_history"

    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"), index=True)
    password_hash: Mapped[str] = mapped_column(String(255))

    user: Mapped["User"] = relationship(back_populates="password_history")


class LoginAttempt(BaseModel):
    __tablename__ = "login_attempts"

    username: Mapped[str] = mapped_column(String(255), index=True)
    ip_address: Mapped[str] = mapped_column(String(50))
    timestamp: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc))
    successful: Mapped[bool] = mapped_column(Boolean)


class WorkflowExecution(BaseModel):
    __tablename__ = "workflow_executions"

    workflow_name: Mapped[str] = mapped_column(String(100), index=True)
    status: Mapped[str] = mapped_column(String(50), default="PENDING")
    started_at: Mapped[datetime | None] = mapped_column(nullable=True)
    finished_at: Mapped[datetime | None] = mapped_column(nullable=True)
    user_id: Mapped[str | None] = mapped_column(ForeignKey("users.id"), nullable=True)
    target: Mapped[str] = mapped_column(String(255), index=True)
    result_summary: Mapped[str | None] = mapped_column(Text, nullable=True)


class AssetRelationship(BaseModel):
    __tablename__ = "asset_relationships"

    parent_asset_id: Mapped[str] = mapped_column(ForeignKey("assets.id"), index=True)
    child_asset_id: Mapped[str] = mapped_column(ForeignKey("assets.id"), index=True)
    relationship_type: Mapped[str] = mapped_column(String(50))

    parent_asset: Mapped["Asset"] = relationship("Asset", foreign_keys=[parent_asset_id])
    child_asset: Mapped["Asset"] = relationship("Asset", foreign_keys=[child_asset_id])


class AssetHistory(BaseModel):
    __tablename__ = "asset_history"

    asset_id: Mapped[str] = mapped_column(ForeignKey("assets.id"), index=True)
    timestamp: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc))
    event: Mapped[str] = mapped_column(String(255))

    asset: Mapped["Asset"] = relationship("Asset", foreign_keys=[asset_id])


class AssetTag(BaseModel):
    __tablename__ = "asset_tags"

    asset_id: Mapped[str] = mapped_column(ForeignKey("assets.id"), index=True)
    tag: Mapped[str] = mapped_column(String(50), index=True)

    asset: Mapped["Asset"] = relationship("Asset", foreign_keys=[asset_id])


class IntelligenceRecord(BaseModel):
    __tablename__ = "intelligence_records"

    asset_id: Mapped[str] = mapped_column(ForeignKey("assets.id"), index=True)
    source: Mapped[str] = mapped_column(String(100))
    data: Mapped[str] = mapped_column(Text)
    confidence: Mapped[int] = mapped_column(default=100)

    asset: Mapped["Asset"] = relationship("Asset", foreign_keys=[asset_id])


class ScheduledReport(BaseModel):
    __tablename__ = "scheduled_reports"

    project_id: Mapped[str] = mapped_column(ForeignKey("projects.id"), index=True)
    report_type: Mapped[str] = mapped_column(String(50))
    frequency: Mapped[str] = mapped_column(String(50))
    last_run: Mapped[datetime | None] = mapped_column(nullable=True)
    next_run: Mapped[datetime | None] = mapped_column(nullable=True)


class DashboardSnapshot(BaseModel):
    __tablename__ = "dashboard_snapshots"

    project_id: Mapped[str] = mapped_column(ForeignKey("projects.id"), index=True)
    timestamp: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc))
    metrics_json: Mapped[str] = mapped_column(Text)


class EventLog(BaseModel):
    __tablename__ = "event_logs"

    event_type: Mapped[str] = mapped_column(String(100), index=True)
    source: Mapped[str] = mapped_column(String(100), default="system")
    severity: Mapped[str] = mapped_column(String(50), default="low")
    timestamp: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc))
    correlation_id: Mapped[str | None] = mapped_column(String(100), index=True, nullable=True)
    payload: Mapped[str] = mapped_column(Text)


class EnrichmentData(BaseModel):
    __tablename__ = "enrichment_data"

    asset_id: Mapped[str] = mapped_column(ForeignKey("assets.id"), index=True)
    enrichment_type: Mapped[str] = mapped_column(String(100))  # e.g., 'tech_guess', 'exposure'
    data: Mapped[dict] = mapped_column(JSON)
    timestamp: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc))

    asset: Mapped["Asset"] = relationship()


class IngestionLog(BaseModel):
    __tablename__ = "ingestion_logs"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    source: Mapped[str] = mapped_column(String(100))
    status: Mapped[str] = mapped_column(String(50))
    records_processed: Mapped[int] = mapped_column(Integer, default=0)
    timestamp: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc))
    details: Mapped[dict | None] = mapped_column(JSON, nullable=True)


class InfrastructureEntity(BaseModel):
    __tablename__ = "infrastructure_entities"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    entity_type: Mapped[str] = mapped_column(
        String(50), index=True
    )  # asn | netblock | organization | certificate
    value: Mapped[str] = mapped_column(String(255), index=True)
    metadata_json: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    timestamp: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc))


class InfraRelation(BaseModel):
    __tablename__ = "infra_relations"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    source_id: Mapped[str] = mapped_column(String(36), index=True)
    target_id: Mapped[str] = mapped_column(String(36), index=True)
    relationship: Mapped[str] = mapped_column(
        String(50)
    )  # ANNOUNCES | OWNS | HOSTS | SIGNED_BY | BELONGS_TO
    timestamp: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc))


class InfraSnapshot(BaseModel):
    __tablename__ = "infra_snapshots"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    snapshot_type: Mapped[str] = mapped_column(String(50))
    data: Mapped[dict] = mapped_column(JSON)
    timestamp: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc))


class EventRule(BaseModel):
    __tablename__ = "event_rules"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    condition_event_type: Mapped[str] = mapped_column(String(100), index=True)
    action_target: Mapped[str] = mapped_column(String(100))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)


class EventQueue(BaseModel):
    __tablename__ = "event_queue"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    event_id: Mapped[str] = mapped_column(String(36), index=True)
    status: Mapped[str] = mapped_column(String(50), default="pending")
    priority: Mapped[str] = mapped_column(String(50), default="medium")
    queued_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc))
    processed_at: Mapped[datetime | None] = mapped_column(nullable=True)


class ExposureProfile(BaseModel):
    __tablename__ = "exposure_profiles"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    asset_id: Mapped[str] = mapped_column(String(36), index=True)
    exposure_level: Mapped[str] = mapped_column(String(100))
    internet_visibility: Mapped[bool] = mapped_column(Boolean, default=True)
    signals: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    timestamp: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc))


class ReputationProfile(BaseModel):
    __tablename__ = "reputation_profiles"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    asset_id: Mapped[str] = mapped_column(String(36), index=True)
    reputation: Mapped[str] = mapped_column(String(50))
    reputation_score: Mapped[int] = mapped_column(Integer, default=0)
    factors: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    timestamp: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc))


class ThreatLink(BaseModel):
    __tablename__ = "threat_links"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    asset_id: Mapped[str] = mapped_column(String(36), index=True)
    threat_tag: Mapped[str] = mapped_column(String(100))
    indicators: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    timestamp: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc))


class IntelCache(BaseModel):
    __tablename__ = "intel_cache"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    lookup_key: Mapped[str] = mapped_column(String(255), index=True, unique=True)
    intel_data: Mapped[dict] = mapped_column(JSON)
    expires_at: Mapped[datetime] = mapped_column()
    timestamp: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc))


class VisualGraph(BaseModel):
    __tablename__ = "visual_graphs"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    graph_type: Mapped[str] = mapped_column(String(100))
    layout_data: Mapped[dict] = mapped_column(JSON)
    timestamp: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc))


class TopologyMap(BaseModel):
    __tablename__ = "topology_maps"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    zone_name: Mapped[str] = mapped_column(String(100))
    assets_included: Mapped[list] = mapped_column(JSON)
    timestamp: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc))


class AssetSnapshot(BaseModel):
    __tablename__ = "asset_snapshots"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    asset_id: Mapped[str] = mapped_column(String(36), index=True)
    snapshot_ref: Mapped[str] = mapped_column(String(255))
    timestamp: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc))


class ClusterMap(BaseModel):
    __tablename__ = "cluster_maps"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    cluster_name: Mapped[str] = mapped_column(String(100))
    assets_included: Mapped[list] = mapped_column(JSON)
    timestamp: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc))


class IOC(BaseModel):
    __tablename__ = "iocs"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    ioc_type: Mapped[str] = mapped_column(String(50))
    value: Mapped[str] = mapped_column(String(255), index=True)
    threat_level: Mapped[str] = mapped_column(String(50))
    source: Mapped[str] = mapped_column(String(100))
    first_seen: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc))
    last_seen: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc))


class ThreatActor(BaseModel):
    __tablename__ = "threat_actors"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    name: Mapped[str] = mapped_column(String(100), index=True)
    aliases: Mapped[list] = mapped_column(JSON)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    timestamp: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc))


class Campaign(BaseModel):
    __tablename__ = "campaigns"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    actor_id: Mapped[str | None] = mapped_column(String(36), index=True, nullable=True)
    name: Mapped[str] = mapped_column(String(100))
    indicators: Mapped[list] = mapped_column(JSON)
    timestamp: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc))


class ThreatMatch(BaseModel):
    __tablename__ = "threat_matches"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    asset_id: Mapped[str] = mapped_column(String(36), index=True)
    ioc_id: Mapped[str | None] = mapped_column(String(36), index=True, nullable=True)
    campaign_id: Mapped[str | None] = mapped_column(String(36), index=True, nullable=True)
    match_score: Mapped[int] = mapped_column(Integer, default=0)
    timestamp: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc))


class VulnerabilitySignal(BaseModel):
    __tablename__ = "vulnerability_signals"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    asset_id: Mapped[str] = mapped_column(String(36), index=True)
    cve_id: Mapped[str | None] = mapped_column(String(50), nullable=True)
    description: Mapped[str] = mapped_column(Text)
    severity: Mapped[str] = mapped_column(String(50))
    timestamp: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc))


class ThreatCache(BaseModel):
    __tablename__ = "threat_cache"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    lookup_key: Mapped[str] = mapped_column(String(255), index=True, unique=True)
    threat_data: Mapped[dict] = mapped_column(JSON)
    expires_at: Mapped[datetime] = mapped_column()
    timestamp: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc))


class CloudAsset(BaseModel):
    __tablename__ = "cloud_assets"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    provider: Mapped[str] = mapped_column(String(50))
    asset_type: Mapped[str] = mapped_column(String(100))
    region: Mapped[str] = mapped_column(String(50))
    exposure_level: Mapped[str] = mapped_column(String(50))
    metadata_json: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    timestamp: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc))


class K8sCluster(BaseModel):
    __tablename__ = "k8s_clusters"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    cluster_name: Mapped[str] = mapped_column(String(100), index=True)
    provider: Mapped[str] = mapped_column(String(50))
    version: Mapped[str] = mapped_column(String(50))
    timestamp: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc))


class K8sNamespace(BaseModel):
    __tablename__ = "k8s_namespaces"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    cluster_id: Mapped[str] = mapped_column(String(36), index=True)
    name: Mapped[str] = mapped_column(String(100))
    timestamp: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc))


class K8sPod(BaseModel):
    __tablename__ = "k8s_pods"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    namespace_id: Mapped[str] = mapped_column(String(36), index=True)
    name: Mapped[str] = mapped_column(String(255))
    status: Mapped[str] = mapped_column(String(50))
    timestamp: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc))


class K8sContainer(BaseModel):
    __tablename__ = "k8s_containers"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    pod_id: Mapped[str] = mapped_column(String(36), index=True)
    image: Mapped[str] = mapped_column(String(255))
    ports: Mapped[list] = mapped_column(JSON)
    timestamp: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc))


class Workload(BaseModel):
    __tablename__ = "workloads"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    name: Mapped[str] = mapped_column(String(255), index=True)
    workload_type: Mapped[str] = mapped_column(String(100))
    exposure: Mapped[str] = mapped_column(String(100))
    dependencies: Mapped[list] = mapped_column(JSON)
    timestamp: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc))


class ServiceMeshEdge(BaseModel):
    __tablename__ = "service_mesh_edges"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    source_service_id: Mapped[str] = mapped_column(String(36), index=True)
    target_service_id: Mapped[str] = mapped_column(String(36), index=True)
    protocol: Mapped[str] = mapped_column(String(50))
    timestamp: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc))


class SecurityEvent(BaseModel):
    __tablename__ = "security_events"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    event_type: Mapped[str] = mapped_column(String(100), index=True)
    source: Mapped[str] = mapped_column(String(100))
    asset_id: Mapped[str | None] = mapped_column(String(36), index=True, nullable=True)
    severity: Mapped[str] = mapped_column(String(50))
    attributes: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    timestamp: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc))


class DetectionRule(BaseModel):
    __tablename__ = "detection_rules"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    severity: Mapped[str] = mapped_column(String(50))
    conditions: Mapped[list] = mapped_column(JSON)
    timestamp: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc))


class Alert(BaseModel):
    __tablename__ = "alerts"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    severity: Mapped[str] = mapped_column(String(50), index=True)
    title: Mapped[str] = mapped_column(String(255))
    entities: Mapped[list] = mapped_column(JSON)
    evidence: Mapped[list] = mapped_column(JSON)
    timestamp: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc))


class BehaviorProfile(BaseModel):
    __tablename__ = "behavior_profiles"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    entity_id: Mapped[str] = mapped_column(String(36), index=True)
    baseline_data: Mapped[dict] = mapped_column(JSON)
    timestamp: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc))


class Anomaly(BaseModel):
    __tablename__ = "anomalies"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    entity_id: Mapped[str] = mapped_column(String(36), index=True)
    anomaly_score: Mapped[int] = mapped_column(Integer)
    details: Mapped[dict] = mapped_column(JSON)
    timestamp: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc))


class Investigation(BaseModel):
    __tablename__ = "investigations"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    title: Mapped[str] = mapped_column(String(255))
    status: Mapped[str] = mapped_column(String(50))
    related_alerts: Mapped[list] = mapped_column(JSON)
    context_data: Mapped[dict] = mapped_column(JSON)
    timestamp: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc))


class Case(BaseModel):
    __tablename__ = "cases"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    title: Mapped[str] = mapped_column(String(255))
    severity: Mapped[str] = mapped_column(String(50))
    status: Mapped[str] = mapped_column(String(50), index=True)
    owner: Mapped[str] = mapped_column(String(100))
    linked_alerts: Mapped[list] = mapped_column(JSON)
    linked_assets: Mapped[list] = mapped_column(JSON)
    timestamp: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc))


class Incident(BaseModel):
    __tablename__ = "incidents"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    case_id: Mapped[str | None] = mapped_column(String(36), index=True, nullable=True)
    title: Mapped[str] = mapped_column(String(255))
    severity: Mapped[str] = mapped_column(String(50))
    status: Mapped[str] = mapped_column(String(50))
    timestamp: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc))


class Evidence(BaseModel):
    __tablename__ = "evidence"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    case_id: Mapped[str] = mapped_column(String(36), index=True)
    evidence_type: Mapped[str] = mapped_column(String(50))
    source: Mapped[str] = mapped_column(String(100))
    references: Mapped[list] = mapped_column(JSON)
    timestamp: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc))


class Playbook(BaseModel):
    __tablename__ = "playbooks"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    severity: Mapped[str] = mapped_column(String(50))
    steps: Mapped[list] = mapped_column(JSON)
    timestamp: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc))


class Workflow(BaseModel):
    __tablename__ = "workflows"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    case_id: Mapped[str] = mapped_column(String(36), index=True)
    task_name: Mapped[str] = mapped_column(String(255))
    assigned_to: Mapped[str] = mapped_column(String(100))
    status: Mapped[str] = mapped_column(String(50))
    timestamp: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc))


class Escalation(BaseModel):
    __tablename__ = "escalations"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    incident_id: Mapped[str] = mapped_column(String(36), index=True)
    priority: Mapped[str] = mapped_column(String(50))
    queue: Mapped[str] = mapped_column(String(100))
    status: Mapped[str] = mapped_column(String(50))
    timestamp: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc))


class KnowledgeBase(BaseModel):
    __tablename__ = "knowledge_base"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    title: Mapped[str] = mapped_column(String(255))
    category: Mapped[str] = mapped_column(String(100))
    content: Mapped[Text] = mapped_column(Text)
    related_cases: Mapped[list] = mapped_column(JSON)
    timestamp: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc))


class BusinessService(BaseModel):
    __tablename__ = "business_services"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    business_unit_id: Mapped[str] = mapped_column(String(36), index=True)
    name: Mapped[str] = mapped_column(String(255))
    criticality: Mapped[str] = mapped_column(String(50))
    owner: Mapped[str] = mapped_column(String(100))
    linked_assets: Mapped[list] = mapped_column(JSON)
    timestamp: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc))


class RiskRegister(BaseModel):
    __tablename__ = "risk_register"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    title: Mapped[str] = mapped_column(String(255))
    business_impact: Mapped[str] = mapped_column(String(50))
    likelihood: Mapped[str] = mapped_column(String(50))
    severity: Mapped[str] = mapped_column(String(50))
    owner: Mapped[str] = mapped_column(String(100))
    status: Mapped[str] = mapped_column(String(50))
    timestamp: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc))


class Control(BaseModel):
    __tablename__ = "controls"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    description: Mapped[Text] = mapped_column(Text)
    framework: Mapped[str] = mapped_column(String(100))
    timestamp: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc))


class ComplianceMapping(BaseModel):
    __tablename__ = "compliance_mappings"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    finding_id: Mapped[str] = mapped_column(String(36), index=True)
    control_id: Mapped[str] = mapped_column(String(36), index=True)
    status: Mapped[str] = mapped_column(String(50))
    timestamp: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc))


class Program(BaseModel):
    __tablename__ = "programs"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    status: Mapped[str] = mapped_column(String(50))
    progress: Mapped[float] = mapped_column(Float, default=0.0)
    timestamp: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc))


class KPI(BaseModel):
    __tablename__ = "kpis"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    metric_name: Mapped[str] = mapped_column(String(100), index=True)
    metric_value: Mapped[float] = mapped_column(Float)
    timestamp: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc))


class ExecutiveReport(BaseModel):
    __tablename__ = "executive_reports"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    title: Mapped[str] = mapped_column(String(255))
    report_type: Mapped[str] = mapped_column(String(50))
    content_json: Mapped[dict] = mapped_column(JSON)
    timestamp: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc))


class Tenant(BaseModel):
    __tablename__ = "tenants"
    name: Mapped[str] = mapped_column(String(255), unique=True)
    status: Mapped[str] = mapped_column(
        String(50), default="ACTIVE"
    )  # ACTIVE, SUSPENDED, ARCHIVED, DELETED
    billing_plan: Mapped[str] = mapped_column(String(50), default="Free")

    users: Mapped[list["User"]] = relationship(back_populates="tenant")
    organizations: Mapped[list["Organization"]] = relationship(
        back_populates="tenant", cascade="all, delete-orphan"
    )
    memberships: Mapped[list["TenantMembership"]] = relationship(
        back_populates="tenant", cascade="all, delete-orphan"
    )


class Organization(BaseModel):
    __tablename__ = "organizations"
    name: Mapped[str] = mapped_column(String(255))
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    tenant_id: Mapped[str | None] = mapped_column(ForeignKey("tenants.id"), index=True)
    tenant: Mapped["Tenant"] = relationship(back_populates="organizations")
    business_units: Mapped[list["BusinessUnit"]] = relationship(
        back_populates="organization", cascade="all, delete-orphan"
    )


class BusinessUnit(BaseModel):
    __tablename__ = "business_units"
    name: Mapped[str] = mapped_column(String(255))
    organization_id: Mapped[str] = mapped_column(ForeignKey("organizations.id"), index=True)

    organization: Mapped["Organization"] = relationship(back_populates="business_units")
    departments: Mapped[list["Department"]] = relationship(
        back_populates="business_unit", cascade="all, delete-orphan"
    )


class Department(BaseModel):
    __tablename__ = "departments"
    name: Mapped[str] = mapped_column(String(255))
    business_unit_id: Mapped[str] = mapped_column(ForeignKey("business_units.id"), index=True)

    business_unit: Mapped["BusinessUnit"] = relationship(back_populates="departments")


class TenantMembership(BaseModel):
    __tablename__ = "tenant_memberships"
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"), index=True)
    # The tenant_id will be inherited from BaseModel, but here we enforce the FK constraint
    tenant_ref_id: Mapped[str] = mapped_column(ForeignKey("tenants.id"), index=True)
    role: Mapped[str] = mapped_column(String(50), default="USER")  # ORG_ADMIN, MSSP_ADMIN, USER

    user: Mapped["User"] = relationship(back_populates="tenant_memberships")
    tenant: Mapped["Tenant"] = relationship(back_populates="memberships")


class Role(BaseModel):
    __tablename__ = "roles"
    name: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    priority: Mapped[int] = mapped_column(Integer, default=0)

    role_permissions: Mapped[list["RolePermission"]] = relationship(
        back_populates="role", cascade="all, delete-orphan"
    )
    user_roles: Mapped[list["UserRole"]] = relationship(
        back_populates="role", cascade="all, delete-orphan"
    )


class Permission(BaseModel):
    __tablename__ = "permissions"
    resource_action: Mapped[str] = mapped_column(
        String(100), unique=True, index=True
    )  # e.g. "asset.read"
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    role_permissions: Mapped[list["RolePermission"]] = relationship(
        back_populates="permission", cascade="all, delete-orphan"
    )


class RolePermission(BaseModel):
    __tablename__ = "role_permissions"
    role_id: Mapped[str] = mapped_column(ForeignKey("roles.id"), index=True)
    permission_id: Mapped[str] = mapped_column(ForeignKey("permissions.id"), index=True)

    role: Mapped["Role"] = relationship(back_populates="role_permissions")
    permission: Mapped["Permission"] = relationship(back_populates="role_permissions")


class UserRole(BaseModel):
    __tablename__ = "user_roles"
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"), index=True)
    role_id: Mapped[str] = mapped_column(ForeignKey("roles.id"), index=True)

    user: Mapped["User"] = relationship(back_populates="user_roles")
    role: Mapped["Role"] = relationship(back_populates="user_roles")


class ReportSchedule(BaseModel):
    __tablename__ = "report_schedules"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    report_type: Mapped[str] = mapped_column(String(100))  # ASM, SOC, Executive
    tenant_id: Mapped[str | None] = mapped_column(String(255), index=True, nullable=True)
    cron_expression: Mapped[str] = mapped_column(String(100))  # e.g. '0 0 * * *'
    distribute_to: Mapped[list | None] = mapped_column(JSON, nullable=True)  # Emails, Webhooks
    status: Mapped[str] = mapped_column(String(50), default="active")
    last_run: Mapped[datetime | None] = mapped_column(nullable=True)
    next_run: Mapped[datetime | None] = mapped_column(nullable=True)
    created_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc))


class SOARWorkflowTemplate(BaseModel):
    __tablename__ = "soar_workflow_templates"
    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    name: Mapped[str] = mapped_column(String(255), unique=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    version: Mapped[int] = mapped_column(Integer, default=1)
    definition_json: Mapped[dict] = mapped_column(JSON)  # Stores trigger, conditions, actions
    tenant_id: Mapped[str | None] = mapped_column(String(255), index=True, nullable=True)
    created_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc))


class SOARWorkflowExecution(BaseModel):
    __tablename__ = "soar_workflow_executions"
    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    workflow_id: Mapped[str] = mapped_column(ForeignKey("soar_workflow_templates.id"), index=True)
    trigger_type: Mapped[str] = mapped_column(String(100))
    status: Mapped[str] = mapped_column(
        String(50), default="Queued"
    )  # Queued, Running, Completed, Failed, Cancelled
    start_time: Mapped[datetime | None] = mapped_column(nullable=True)
    end_time: Mapped[datetime | None] = mapped_column(nullable=True)
    tenant_id: Mapped[str | None] = mapped_column(String(255), index=True, nullable=True)
    logs: Mapped[list | None] = mapped_column(JSON, nullable=True)


class SOARTaskExecution(BaseModel):
    __tablename__ = "soar_task_executions"
    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    execution_id: Mapped[str] = mapped_column(ForeignKey("soar_workflow_executions.id"), index=True)
    celery_task_id: Mapped[str] = mapped_column(String(255), index=True)
    task_name: Mapped[str] = mapped_column(String(255))
    status: Mapped[str] = mapped_column(String(50), default="Pending")
    result: Mapped[dict | None] = mapped_column(JSON, nullable=True)


class Notification(BaseModel):
    __tablename__ = "notifications"
    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"), index=True)
    title: Mapped[str] = mapped_column(String(255))
    message: Mapped[str] = mapped_column(Text)
    type: Mapped[str] = mapped_column(String(50))  # e.g. alert, report, finding
    is_read: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    link: Mapped[str | None] = mapped_column(String(255), nullable=True)
    metadata_json: Mapped[dict | None] = mapped_column(JSON, nullable=True)
