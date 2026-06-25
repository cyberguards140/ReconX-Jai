from enum import Enum

from pydantic import BaseModel, Field


class SeverityEnum(str, Enum):
    critical = "critical"
    high = "high"
    medium = "medium"
    low = "low"
    info = "info"


class NormalizedAsset(BaseModel):
    asset_type: str = Field(..., description="e.g., ip, domain, url")
    value: str = Field(..., description="The actual value of the asset")
    hostname: str | None = None
    mac_address: str | None = None
    registrar: str | None = None
    created_at: str | None = None
    expires_at: str | None = None
    is_resolved: bool | None = False
    organization: str | None = None
    source_tool: str | None = None
    sources: list[str] | None = None


class NormalizedPort(BaseModel):
    port: int
    protocol: str = "tcp"
    state: str = "open"


class NormalizedService(BaseModel):
    port: int
    service: str
    product: str | None = None
    version: str | None = None


class NormalizedTechnology(BaseModel):
    technology: str
    version: str | None = None
    service_port: int | None = None


class NormalizedCMS(BaseModel):
    cms: str
    version: str | None = None
    service_port: int | None = None


class NormalizedFramework(BaseModel):
    framework: str
    version: str | None = None
    service_port: int | None = None


class NormalizedWAF(BaseModel):
    vendor: str
    detected: bool = True
    service_port: int | None = None


class NormalizedHeader(BaseModel):
    name: str
    value: str
    is_security: bool = False
    service_port: int | None = None


class NormalizedCertificate(BaseModel):
    issuer: str
    subject: str
    valid_from: str | None = None
    valid_until: str | None = None
    san_entries: list[str] | None = None
    service_port: int | None = None


class NormalizedTLSConfiguration(BaseModel):
    protocol: str
    enabled: bool = True
    service_port: int | None = None


class NormalizedCipherSuite(BaseModel):
    protocol: str
    cipher: str
    strength: str
    service_port: int | None = None


class NormalizedSMBHost(BaseModel):
    hostname: str
    domain: str | None = None
    os: str | None = None
    source_tool: str | None = None
    sources: list[str] | None = None


class NormalizedSMBShare(BaseModel):
    share_name: str
    comment: str | None = None
    type: str | None = None
    source_tool: str | None = None
    sources: list[str] | None = None


class NormalizedSMBUser(BaseModel):
    username: str
    source_tool: str | None = None
    sources: list[str] | None = None


class NormalizedSMBGroup(BaseModel):
    group_name: str
    source_tool: str | None = None
    sources: list[str] | None = None


class NormalizedSMBPasswordPolicy(BaseModel):
    minimum_length: int | None = None
    lockout_enabled: bool | None = None
    source_tool: str | None = None
    sources: list[str] | None = None


class NormalizedSMBConfiguration(BaseModel):
    signing_required: bool | None = None
    smbv1_enabled: bool | None = None
    source_tool: str | None = None
    sources: list[str] | None = None


class NormalizedADDomain(BaseModel):
    domain_name: str
    forest: str | None = None
    source_tool: str | None = None
    sources: list[str] | None = None


class NormalizedADUser(BaseModel):
    domain: str
    username: str
    display_name: str | None = None
    source_tool: str | None = None
    sources: list[str] | None = None


class NormalizedADGroup(BaseModel):
    domain: str
    group_name: str
    members_count: int | None = None
    source_tool: str | None = None
    sources: list[str] | None = None


class NormalizedADComputer(BaseModel):
    domain: str
    hostname: str
    os: str | None = None
    source_tool: str | None = None
    sources: list[str] | None = None


class NormalizedADOrganizationalUnit(BaseModel):
    domain: str
    ou_name: str
    source_tool: str | None = None
    sources: list[str] | None = None


class NormalizedADTrustRelationship(BaseModel):
    source_domain: str
    target_domain: str
    trust_type: str | None = None
    source_tool: str | None = None
    sources: list[str] | None = None


class NormalizedOSINTOrganization(BaseModel):
    organization: str
    source_tool: str | None = None
    sources: list[str] | None = None


class NormalizedOSINTEmail(BaseModel):
    email: str
    source_tool: str | None = None
    sources: list[str] | None = None


class NormalizedOSINTUsername(BaseModel):
    username: str
    source_tool: str | None = None
    sources: list[str] | None = None


class NormalizedOSINTProfile(BaseModel):
    username: str
    platform: str
    profile_url: str | None = None
    source_tool: str | None = None
    sources: list[str] | None = None


class NormalizedOSINTRelationship(BaseModel):
    source_entity: str
    target_entity: str
    relationship_type: str
    source_tool: str | None = None
    sources: list[str] | None = None


class NormalizedTrafficFlow(BaseModel):
    src_ip: str
    dst_ip: str
    protocol: str
    source_tool: str | None = None
    sources: list[str] | None = None


class NormalizedTrafficProtocol(BaseModel):
    protocol: str
    source_tool: str | None = None
    sources: list[str] | None = None


class NormalizedTrafficCommunication(BaseModel):
    host_a: str
    host_b: str
    protocol: str
    source_tool: str | None = None
    sources: list[str] | None = None


class NormalizedTrafficDNSQuery(BaseModel):
    domain: str
    query_type: str | None = None
    source_tool: str | None = None
    sources: list[str] | None = None


class NormalizedTrafficHTTPMetadata(BaseModel):
    host: str
    method: str
    uri: str | None = None
    source_tool: str | None = None
    sources: list[str] | None = None


class NormalizedTrafficTLSMetadata(BaseModel):
    sni: str
    tls_version: str | None = None
    source_tool: str | None = None
    sources: list[str] | None = None


class NormalizedTrafficStatistic(BaseModel):
    stat_name: str
    stat_value: str
    source_tool: str | None = None
    sources: list[str] | None = None


class NormalizedCloudAccount(BaseModel):
    provider: str
    account_id: str
    source_tool: str | None = None
    sources: list[str] | None = None


class NormalizedCloudResource(BaseModel):
    account_id: str
    resource_type: str
    resource_id: str
    source_tool: str | None = None
    sources: list[str] | None = None


class NormalizedCloudKubernetesCluster(BaseModel):
    cluster_name: str
    source_tool: str | None = None
    sources: list[str] | None = None


class NormalizedCloudNamespace(BaseModel):
    cluster_name: str
    namespace: str
    source_tool: str | None = None
    sources: list[str] | None = None


class NormalizedCloudPod(BaseModel):
    namespace: str
    pod_name: str
    source_tool: str | None = None
    sources: list[str] | None = None


class NormalizedCloudDeployment(BaseModel):
    namespace: str
    deployment_name: str
    source_tool: str | None = None
    sources: list[str] | None = None


class NormalizedCloudContainerImage(BaseModel):
    image: str
    tag: str | None = None
    source_tool: str | None = None
    sources: list[str] | None = None


class NormalizedCloudContainerFinding(BaseModel):
    image: str
    vulnerability_id: str
    severity: str | None = None
    source_tool: str | None = None
    sources: list[str] | None = None


class NormalizedVulnCVE(BaseModel):
    cve_id: str
    title: str | None = None
    cvss_score: float | None = None
    severity: str | None = None
    source_tool: str | None = None
    sources: list[str] | None = None


class NormalizedVulnCPE(BaseModel):
    cpe_string: str
    product: str | None = None
    version: str | None = None
    source_tool: str | None = None
    sources: list[str] | None = None


class NormalizedVulnRecord(BaseModel):
    asset_id: str
    cve_id: str | None = None
    title: str
    severity: str | None = None
    source_tool: str | None = None
    sources: list[str] | None = None


class NormalizedVulnRiskProfile(BaseModel):
    asset_id: str
    risk_score: float = 0.0
    critical_count: int = 0
    high_count: int = 0
    medium_count: int = 0
    low_count: int = 0
    source_tool: str | None = None
    sources: list[str] | None = None


class NormalizedVulnEvidence(BaseModel):
    finding_id: str
    evidence_data: str
    source_tool: str | None = None
    sources: list[str] | None = None


class NormalizedVulnReference(BaseModel):
    entity_id: str
    url: str
    source_tool: str | None = None
    sources: list[str] | None = None


class NormalizedContent(BaseModel):
    url: str
    path: str
    status_code: int = 200
    content_length: int | None = None
    content_type: str | None = None
    service_port: int | None = None
    technology: str | None = None
    source_tool: str | None = None
    sources: list[str] | None = None


class NormalizedEndpoint(BaseModel):
    method: str
    path: str
    service_port: int | None = None
    source_tool: str | None = None
    sources: list[str] | None = None


class NormalizedVirtualHost(BaseModel):
    vhost: str
    service_port: int | None = None
    source_tool: str | None = None
    sources: list[str] | None = None


class NormalizedScreenshot(BaseModel):
    path: str
    title: str | None = None


class NormalizedFinding(BaseModel):
    title: str
    description: str
    severity: str
    evidence: str | None = None
    source_tool: str | None = None


class NormalizedRoute(BaseModel):
    hop_count: int
    node_ip: str
    latency: float | None = None


class NormalizedDNSRecord(BaseModel):
    record_type: str
    value: str


class NormalizedRecord(BaseModel):
    """A complete record encompassing an asset and its discovered properties."""

    asset: NormalizedAsset
    ports: list[NormalizedPort] = []
    services: list[NormalizedService] = []
    technologies: list[NormalizedTechnology] = []
    cms: list[NormalizedCMS] = []
    frameworks: list[NormalizedFramework] = []
    wafs: list[NormalizedWAF] = []
    headers: list[NormalizedHeader] = []
    certificates: list[NormalizedCertificate] = []
    tls_configurations: list[NormalizedTLSConfiguration] = []
    cipher_suites: list[NormalizedCipherSuite] = []
    smb_hosts: list[NormalizedSMBHost] = []
    smb_shares: list[NormalizedSMBShare] = []
    smb_users: list[NormalizedSMBUser] = []
    smb_groups: list[NormalizedSMBGroup] = []
    smb_password_policies: list[NormalizedSMBPasswordPolicy] = []
    smb_configurations: list[NormalizedSMBConfiguration] = []
    ad_domains: list[NormalizedADDomain] = []
    ad_users: list[NormalizedADUser] = []
    ad_groups: list[NormalizedADGroup] = []
    ad_computers: list[NormalizedADComputer] = []
    ad_organizational_units: list[NormalizedADOrganizationalUnit] = []
    ad_trust_relationships: list[NormalizedADTrustRelationship] = []
    osint_organizations: list[NormalizedOSINTOrganization] = []
    osint_emails: list[NormalizedOSINTEmail] = []
    osint_usernames: list[NormalizedOSINTUsername] = []
    osint_profiles: list[NormalizedOSINTProfile] = []
    osint_relationships: list[NormalizedOSINTRelationship] = []
    traffic_flows: list[NormalizedTrafficFlow] = []
    traffic_protocols: list[NormalizedTrafficProtocol] = []
    traffic_communications: list[NormalizedTrafficCommunication] = []
    traffic_dns_queries: list[NormalizedTrafficDNSQuery] = []
    traffic_http_metadata: list[NormalizedTrafficHTTPMetadata] = []
    traffic_tls_metadata: list[NormalizedTrafficTLSMetadata] = []
    traffic_statistics: list[NormalizedTrafficStatistic] = []
    cloud_accounts: list[NormalizedCloudAccount] = []
    cloud_resources: list[NormalizedCloudResource] = []
    cloud_kubernetes_clusters: list[NormalizedCloudKubernetesCluster] = []
    cloud_namespaces: list[NormalizedCloudNamespace] = []
    cloud_pods: list[NormalizedCloudPod] = []
    cloud_deployments: list[NormalizedCloudDeployment] = []
    cloud_container_images: list[NormalizedCloudContainerImage] = []
    cloud_container_findings: list[NormalizedCloudContainerFinding] = []
    vuln_cves: list[NormalizedVulnCVE] = []
    vuln_cpes: list[NormalizedVulnCPE] = []
    vuln_records: list[NormalizedVulnRecord] = []
    vuln_risk_profiles: list[NormalizedVulnRiskProfile] = []
    vuln_evidence: list[NormalizedVulnEvidence] = []
    vuln_references: list[NormalizedVulnReference] = []
    contents: list[NormalizedContent] = []
    endpoints: list[NormalizedEndpoint] = []
    vhosts: list[NormalizedVirtualHost] = []
    screenshots: list[NormalizedScreenshot] = []
    findings: list[NormalizedFinding] = []
    routes: list[NormalizedRoute] = []
    dns_records: list[NormalizedDNSRecord] = []
