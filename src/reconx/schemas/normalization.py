from pydantic import BaseModel, Field
from typing import Optional, List
from enum import Enum

class SeverityEnum(str, Enum):
    critical = "critical"
    high = "high"
    medium = "medium"
    low = "low"
    info = "info"

class NormalizedAsset(BaseModel):
    asset_type: str = Field(..., description="e.g., ip, domain, url")
    value: str = Field(..., description="The actual value of the asset")
    hostname: Optional[str] = None
    mac_address: Optional[str] = None
    registrar: Optional[str] = None
    created_at: Optional[str] = None
    expires_at: Optional[str] = None
    is_resolved: Optional[bool] = False
    organization: Optional[str] = None
    source_tool: Optional[str] = None
    sources: Optional[List[str]] = None

class NormalizedPort(BaseModel):
    port: int
    protocol: str = "tcp"
    state: str = "open"

class NormalizedService(BaseModel):
    port: int
    service: str
    product: Optional[str] = None
    version: Optional[str] = None

class NormalizedTechnology(BaseModel):
    technology: str
    version: Optional[str] = None
    service_port: Optional[int] = None

class NormalizedCMS(BaseModel):
    cms: str
    version: Optional[str] = None
    service_port: Optional[int] = None

class NormalizedFramework(BaseModel):
    framework: str
    version: Optional[str] = None
    service_port: Optional[int] = None

class NormalizedWAF(BaseModel):
    vendor: str
    detected: bool = True
    service_port: Optional[int] = None

class NormalizedHeader(BaseModel):
    name: str
    value: str
    is_security: bool = False
    service_port: Optional[int] = None

class NormalizedCertificate(BaseModel):
    issuer: str
    subject: str
    valid_from: Optional[str] = None
    valid_until: Optional[str] = None
    san_entries: Optional[List[str]] = None
    service_port: Optional[int] = None

class NormalizedTLSConfiguration(BaseModel):
    protocol: str
    enabled: bool = True
    service_port: Optional[int] = None

class NormalizedCipherSuite(BaseModel):
    protocol: str
    cipher: str
    strength: str
    service_port: Optional[int] = None

class NormalizedSMBHost(BaseModel):
    hostname: str
    domain: Optional[str] = None
    os: Optional[str] = None
    source_tool: Optional[str] = None
    sources: Optional[List[str]] = None

class NormalizedSMBShare(BaseModel):
    share_name: str
    comment: Optional[str] = None
    type: Optional[str] = None
    source_tool: Optional[str] = None
    sources: Optional[List[str]] = None

class NormalizedSMBUser(BaseModel):
    username: str
    source_tool: Optional[str] = None
    sources: Optional[List[str]] = None

class NormalizedSMBGroup(BaseModel):
    group_name: str
    source_tool: Optional[str] = None
    sources: Optional[List[str]] = None

class NormalizedSMBPasswordPolicy(BaseModel):
    minimum_length: Optional[int] = None
    lockout_enabled: Optional[bool] = None
    source_tool: Optional[str] = None
    sources: Optional[List[str]] = None

class NormalizedSMBConfiguration(BaseModel):
    signing_required: Optional[bool] = None
    smbv1_enabled: Optional[bool] = None
    source_tool: Optional[str] = None
    sources: Optional[List[str]] = None

class NormalizedADDomain(BaseModel):
    domain_name: str
    forest: Optional[str] = None
    source_tool: Optional[str] = None
    sources: Optional[List[str]] = None

class NormalizedADUser(BaseModel):
    domain: str
    username: str
    display_name: Optional[str] = None
    source_tool: Optional[str] = None
    sources: Optional[List[str]] = None

class NormalizedADGroup(BaseModel):
    domain: str
    group_name: str
    members_count: Optional[int] = None
    source_tool: Optional[str] = None
    sources: Optional[List[str]] = None

class NormalizedADComputer(BaseModel):
    domain: str
    hostname: str
    os: Optional[str] = None
    source_tool: Optional[str] = None
    sources: Optional[List[str]] = None

class NormalizedADOrganizationalUnit(BaseModel):
    domain: str
    ou_name: str
    source_tool: Optional[str] = None
    sources: Optional[List[str]] = None

class NormalizedADTrustRelationship(BaseModel):
    source_domain: str
    target_domain: str
    trust_type: Optional[str] = None
    source_tool: Optional[str] = None
    sources: Optional[List[str]] = None

class NormalizedOSINTOrganization(BaseModel):
    organization: str
    source_tool: Optional[str] = None
    sources: Optional[List[str]] = None

class NormalizedOSINTEmail(BaseModel):
    email: str
    source_tool: Optional[str] = None
    sources: Optional[List[str]] = None

class NormalizedOSINTUsername(BaseModel):
    username: str
    source_tool: Optional[str] = None
    sources: Optional[List[str]] = None

class NormalizedOSINTProfile(BaseModel):
    username: str
    platform: str
    profile_url: Optional[str] = None
    source_tool: Optional[str] = None
    sources: Optional[List[str]] = None

class NormalizedOSINTRelationship(BaseModel):
    source_entity: str
    target_entity: str
    relationship_type: str
    source_tool: Optional[str] = None
    sources: Optional[List[str]] = None

class NormalizedTrafficFlow(BaseModel):
    src_ip: str
    dst_ip: str
    protocol: str
    source_tool: Optional[str] = None
    sources: Optional[List[str]] = None

class NormalizedTrafficProtocol(BaseModel):
    protocol: str
    source_tool: Optional[str] = None
    sources: Optional[List[str]] = None

class NormalizedTrafficCommunication(BaseModel):
    host_a: str
    host_b: str
    protocol: str
    source_tool: Optional[str] = None
    sources: Optional[List[str]] = None

class NormalizedTrafficDNSQuery(BaseModel):
    domain: str
    query_type: Optional[str] = None
    source_tool: Optional[str] = None
    sources: Optional[List[str]] = None

class NormalizedTrafficHTTPMetadata(BaseModel):
    host: str
    method: str
    uri: Optional[str] = None
    source_tool: Optional[str] = None
    sources: Optional[List[str]] = None

class NormalizedTrafficTLSMetadata(BaseModel):
    sni: str
    tls_version: Optional[str] = None
    source_tool: Optional[str] = None
    sources: Optional[List[str]] = None

class NormalizedTrafficStatistic(BaseModel):
    stat_name: str
    stat_value: str
    source_tool: Optional[str] = None
    sources: Optional[List[str]] = None

class NormalizedCloudAccount(BaseModel):
    provider: str
    account_id: str
    source_tool: Optional[str] = None
    sources: Optional[List[str]] = None

class NormalizedCloudResource(BaseModel):
    account_id: str
    resource_type: str
    resource_id: str
    source_tool: Optional[str] = None
    sources: Optional[List[str]] = None

class NormalizedCloudKubernetesCluster(BaseModel):
    cluster_name: str
    source_tool: Optional[str] = None
    sources: Optional[List[str]] = None

class NormalizedCloudNamespace(BaseModel):
    cluster_name: str
    namespace: str
    source_tool: Optional[str] = None
    sources: Optional[List[str]] = None

class NormalizedCloudPod(BaseModel):
    namespace: str
    pod_name: str
    source_tool: Optional[str] = None
    sources: Optional[List[str]] = None

class NormalizedCloudDeployment(BaseModel):
    namespace: str
    deployment_name: str
    source_tool: Optional[str] = None
    sources: Optional[List[str]] = None

class NormalizedCloudContainerImage(BaseModel):
    image: str
    tag: Optional[str] = None
    source_tool: Optional[str] = None
    sources: Optional[List[str]] = None

class NormalizedCloudContainerFinding(BaseModel):
    image: str
    vulnerability_id: str
    severity: Optional[str] = None
    source_tool: Optional[str] = None
    sources: Optional[List[str]] = None

class NormalizedVulnCVE(BaseModel):
    cve_id: str
    title: Optional[str] = None
    cvss_score: Optional[float] = None
    severity: Optional[str] = None
    source_tool: Optional[str] = None
    sources: Optional[List[str]] = None

class NormalizedVulnCPE(BaseModel):
    cpe_string: str
    product: Optional[str] = None
    version: Optional[str] = None
    source_tool: Optional[str] = None
    sources: Optional[List[str]] = None

class NormalizedVulnRecord(BaseModel):
    asset_id: str
    cve_id: Optional[str] = None
    title: str
    severity: Optional[str] = None
    source_tool: Optional[str] = None
    sources: Optional[List[str]] = None

class NormalizedVulnRiskProfile(BaseModel):
    asset_id: str
    risk_score: float = 0.0
    critical_count: int = 0
    high_count: int = 0
    medium_count: int = 0
    low_count: int = 0
    source_tool: Optional[str] = None
    sources: Optional[List[str]] = None

class NormalizedVulnEvidence(BaseModel):
    finding_id: str
    evidence_data: str
    source_tool: Optional[str] = None
    sources: Optional[List[str]] = None

class NormalizedVulnReference(BaseModel):
    entity_id: str
    url: str
    source_tool: Optional[str] = None
    sources: Optional[List[str]] = None

class NormalizedContent(BaseModel):
    url: str
    path: str
    status_code: int = 200
    content_length: Optional[int] = None
    content_type: Optional[str] = None
    service_port: Optional[int] = None
    technology: Optional[str] = None
    source_tool: Optional[str] = None
    sources: Optional[List[str]] = None

class NormalizedEndpoint(BaseModel):
    method: str
    path: str
    service_port: Optional[int] = None
    source_tool: Optional[str] = None
    sources: Optional[List[str]] = None

class NormalizedVirtualHost(BaseModel):
    vhost: str
    service_port: Optional[int] = None
    source_tool: Optional[str] = None
    sources: Optional[List[str]] = None

class NormalizedScreenshot(BaseModel):
    path: str
    title: Optional[str] = None

class NormalizedFinding(BaseModel):
    title: str
    description: str
    severity: str
    evidence: Optional[str] = None
    source_tool: Optional[str] = None

class NormalizedRoute(BaseModel):
    hop_count: int
    node_ip: str
    latency: Optional[float] = None

class NormalizedDNSRecord(BaseModel):
    record_type: str
    value: str

class NormalizedRecord(BaseModel):
    """A complete record encompassing an asset and its discovered properties."""
    asset: NormalizedAsset
    ports: List[NormalizedPort] = []
    services: List[NormalizedService] = []
    technologies: List[NormalizedTechnology] = []
    cms: List[NormalizedCMS] = []
    frameworks: List[NormalizedFramework] = []
    wafs: List[NormalizedWAF] = []
    headers: List[NormalizedHeader] = []
    certificates: List[NormalizedCertificate] = []
    tls_configurations: List[NormalizedTLSConfiguration] = []
    cipher_suites: List[NormalizedCipherSuite] = []
    smb_hosts: List[NormalizedSMBHost] = []
    smb_shares: List[NormalizedSMBShare] = []
    smb_users: List[NormalizedSMBUser] = []
    smb_groups: List[NormalizedSMBGroup] = []
    smb_password_policies: List[NormalizedSMBPasswordPolicy] = []
    smb_configurations: List[NormalizedSMBConfiguration] = []
    ad_domains: List[NormalizedADDomain] = []
    ad_users: List[NormalizedADUser] = []
    ad_groups: List[NormalizedADGroup] = []
    ad_computers: List[NormalizedADComputer] = []
    ad_organizational_units: List[NormalizedADOrganizationalUnit] = []
    ad_trust_relationships: List[NormalizedADTrustRelationship] = []
    osint_organizations: List[NormalizedOSINTOrganization] = []
    osint_emails: List[NormalizedOSINTEmail] = []
    osint_usernames: List[NormalizedOSINTUsername] = []
    osint_profiles: List[NormalizedOSINTProfile] = []
    osint_relationships: List[NormalizedOSINTRelationship] = []
    traffic_flows: List[NormalizedTrafficFlow] = []
    traffic_protocols: List[NormalizedTrafficProtocol] = []
    traffic_communications: List[NormalizedTrafficCommunication] = []
    traffic_dns_queries: List[NormalizedTrafficDNSQuery] = []
    traffic_http_metadata: List[NormalizedTrafficHTTPMetadata] = []
    traffic_tls_metadata: List[NormalizedTrafficTLSMetadata] = []
    traffic_statistics: List[NormalizedTrafficStatistic] = []
    cloud_accounts: List[NormalizedCloudAccount] = []
    cloud_resources: List[NormalizedCloudResource] = []
    cloud_kubernetes_clusters: List[NormalizedCloudKubernetesCluster] = []
    cloud_namespaces: List[NormalizedCloudNamespace] = []
    cloud_pods: List[NormalizedCloudPod] = []
    cloud_deployments: List[NormalizedCloudDeployment] = []
    cloud_container_images: List[NormalizedCloudContainerImage] = []
    cloud_container_findings: List[NormalizedCloudContainerFinding] = []
    vuln_cves: List[NormalizedVulnCVE] = []
    vuln_cpes: List[NormalizedVulnCPE] = []
    vuln_records: List[NormalizedVulnRecord] = []
    vuln_risk_profiles: List[NormalizedVulnRiskProfile] = []
    vuln_evidence: List[NormalizedVulnEvidence] = []
    vuln_references: List[NormalizedVulnReference] = []
    contents: List[NormalizedContent] = []
    endpoints: List[NormalizedEndpoint] = []
    vhosts: List[NormalizedVirtualHost] = []
    screenshots: List[NormalizedScreenshot] = []
    findings: List[NormalizedFinding] = []
    routes: List[NormalizedRoute] = []
    dns_records: List[NormalizedDNSRecord] = []
