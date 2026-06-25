from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Dict, Any
from reconx.services.intelligence.intelligence_store import IntelligenceStore
from reconx.reporting.executive_summary import ExecutiveSummaryGenerator
from reconx.reporting.dashboard_service import DashboardService
from reconx.database.models import Port, Service, Route, DNSRecord, AssetRelationship, Technology, CMS, Framework, WAF, HTTPHeader, ContentItem, Endpoint, VirtualHost, Certificate, TLSConfiguration, CipherSuite, Finding, SMBHost, SMBShare, SMBUser, SMBGroup, SMBPasswordPolicy, SMBConfiguration, ADDomain, ADUser, ADGroup, ADComputer, ADOrganizationalUnit, ADTrustRelationship, OSINTOrganization, OSINTEmail, OSINTUsername, OSINTProfile, OSINTRelationship, TrafficFlow, TrafficProtocol, TrafficCommunication, TrafficDNSQuery, TrafficHTTPMetadata, TrafficTLSMetadata, TrafficStatistic, CloudAccount, CloudResource, CloudKubernetesCluster, CloudNamespace, CloudPod, CloudDeployment, CloudContainerImage, CloudContainerFinding, VulnCVE, VulnCPE, VulnRecord, VulnRiskProfile, VulnEvidence, VulnReference

class ReportBuilder:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.store = IntelligenceStore(db)
        self.dashboard = DashboardService(db)

    async def build_executive_data(self) -> Dict[str, Any]:
        assets = await self.store.get_assets()
        metrics = await self.dashboard.get_metrics()
        
        # Load detailed inventory for the report
        port_result = await self.db.execute(select(Port))
        ports = port_result.scalars().all()
        
        service_result = await self.db.execute(select(Service))
        services = service_result.scalars().all()

        route_result = await self.db.execute(select(Route))
        routes = route_result.scalars().all()

        dns_result = await self.db.execute(select(DNSRecord))
        dns_records = dns_result.scalars().all()
        
        rel_result = await self.db.execute(select(AssetRelationship))
        relationships = rel_result.scalars().all()

        tech_res = await self.db.execute(select(Technology))
        cms_res = await self.db.execute(select(CMS))
        fw_res = await self.db.execute(select(Framework))
        waf_res = await self.db.execute(select(WAF))
        hdr_res = await self.db.execute(select(HTTPHeader))

        content_res = await self.db.execute(select(ContentItem))
        endp_res = await self.db.execute(select(Endpoint))
        vhost_res = await self.db.execute(select(VirtualHost))

        cert_res = await self.db.execute(select(Certificate))
        tls_res = await self.db.execute(select(TLSConfiguration))
        cipher_res = await self.db.execute(select(CipherSuite))
        findings_res = await self.db.execute(select(Finding))

        smb_host_res = await self.db.execute(select(SMBHost))
        smb_share_res = await self.db.execute(select(SMBShare))
        smb_user_res = await self.db.execute(select(SMBUser))
        smb_group_res = await self.db.execute(select(SMBGroup))
        smb_pw_res = await self.db.execute(select(SMBPasswordPolicy))
        smb_conf_res = await self.db.execute(select(SMBConfiguration))

        ad_dom_res = await self.db.execute(select(ADDomain))
        ad_user_res = await self.db.execute(select(ADUser))
        ad_group_res = await self.db.execute(select(ADGroup))
        ad_comp_res = await self.db.execute(select(ADComputer))
        ad_ou_res = await self.db.execute(select(ADOrganizationalUnit))
        ad_trust_res = await self.db.execute(select(ADTrustRelationship))

        osint_org_res = await self.db.execute(select(OSINTOrganization))
        osint_email_res = await self.db.execute(select(OSINTEmail))
        osint_uname_res = await self.db.execute(select(OSINTUsername))
        osint_prof_res = await self.db.execute(select(OSINTProfile))
        osint_rel_res = await self.db.execute(select(OSINTRelationship))

        traffic_flow_res = await self.db.execute(select(TrafficFlow))
        traffic_proto_res = await self.db.execute(select(TrafficProtocol))
        traffic_comm_res = await self.db.execute(select(TrafficCommunication))
        traffic_dns_res = await self.db.execute(select(TrafficDNSQuery))
        traffic_http_res = await self.db.execute(select(TrafficHTTPMetadata))
        traffic_tls_res = await self.db.execute(select(TrafficTLSMetadata))
        traffic_stat_res = await self.db.execute(select(TrafficStatistic))

        cloud_acc_res = await self.db.execute(select(CloudAccount))
        cloud_res_res = await self.db.execute(select(CloudResource))
        cloud_k8s_res = await self.db.execute(select(CloudKubernetesCluster))
        cloud_ns_res = await self.db.execute(select(CloudNamespace))
        cloud_pod_res = await self.db.execute(select(CloudPod))
        cloud_dep_res = await self.db.execute(select(CloudDeployment))
        cloud_img_res = await self.db.execute(select(CloudContainerImage))
        cloud_find_res = await self.db.execute(select(CloudContainerFinding))

        vuln_cve_res = await self.db.execute(select(VulnCVE))
        vuln_cpe_res = await self.db.execute(select(VulnCPE))
        vuln_rec_res = await self.db.execute(select(VulnRecord))
        vuln_prof_res = await self.db.execute(select(VulnRiskProfile))
        vuln_ev_res = await self.db.execute(select(VulnEvidence))
        vuln_ref_res = await self.db.execute(select(VulnReference))

        mock_findings = [{"severity": "CRITICAL"}] * metrics.get(
            "critical_findings", 0
        ) + [{"severity": "HIGH"}] * metrics.get("high_findings", 0)

        exec_summary = ExecutiveSummaryGenerator.generate(
            assets, mock_findings, metrics.get("risk_score", 0)
        )

        return {
            "project": "Default Project",
            "executive_summary": exec_summary,
            "assets": assets,
            "domain_inventory": [a for a in assets if a.asset_type == "domain"],
            "subdomain_inventory": [a for a in assets if a.asset_type == "subdomain"],
            "infrastructure": {
                "asns": [a for a in assets if a.asset_type == "asn"],
                "netblocks": [a for a in assets if a.asset_type == "netblock"]
            },
            "host_inventory": [a for a in assets if a.asset_type == "ip"],
            "open_ports": ports,
            "services": services,
            "network_paths": routes,
            "dns_records": dns_records,
            "domain_relationships": relationships,
            "discovery_sources": metrics.get("top_discovery_sources", {}),
            "web_technologies": tech_res.scalars().all(),
            "cms": cms_res.scalars().all(),
            "frameworks": fw_res.scalars().all(),
            "waf_detection": waf_res.scalars().all(),
            "http_headers": hdr_res.scalars().all(),
            "content_discovery": {
                "directories_and_files": content_res.scalars().all(),
                "endpoints": endp_res.scalars().all(),
                "virtual_hosts": vhost_res.scalars().all()
            },
            "web_assessment": {
                "certificates": cert_res.scalars().all(),
                "tls_configurations": tls_res.scalars().all(),
                "cipher_suites": cipher_res.scalars().all(),
                "findings": findings_res.scalars().all()
            },
            "smb_intelligence": {
                "hosts": smb_host_res.scalars().all(),
                "shares": smb_share_res.scalars().all(),
                "users": smb_user_res.scalars().all(),
                "groups": smb_group_res.scalars().all(),
                "password_policies": smb_pw_res.scalars().all(),
                "configurations": smb_conf_res.scalars().all()
            },
            "active_directory": {
                "domains": ad_dom_res.scalars().all(),
                "users": ad_user_res.scalars().all(),
                "groups": ad_group_res.scalars().all(),
                "computers": ad_comp_res.scalars().all(),
                "organizational_units": ad_ou_res.scalars().all(),
                "trusts": ad_trust_res.scalars().all()
            },
            "osint": {
                "organizations": osint_org_res.scalars().all(),
                "emails": osint_email_res.scalars().all(),
                "usernames": osint_uname_res.scalars().all(),
                "profiles": osint_prof_res.scalars().all(),
                "relationships": osint_rel_res.scalars().all()
            },
            "packet_analysis": {
                "flows": traffic_flow_res.scalars().all(),
                "protocols": traffic_proto_res.scalars().all(),
                "communications": traffic_comm_res.scalars().all(),
                "dns_queries": traffic_dns_res.scalars().all(),
                "http_metadata": traffic_http_res.scalars().all(),
                "tls_metadata": traffic_tls_res.scalars().all(),
                "statistics": traffic_stat_res.scalars().all()
            },
            "cloud_container": {
                "accounts": cloud_acc_res.scalars().all(),
                "resources": cloud_res_res.scalars().all(),
                "kubernetes_clusters": cloud_k8s_res.scalars().all(),
                "namespaces": cloud_ns_res.scalars().all(),
                "pods": cloud_pod_res.scalars().all(),
                "deployments": cloud_dep_res.scalars().all(),
                "container_images": cloud_img_res.scalars().all(),
                "container_findings": cloud_find_res.scalars().all()
            },
            "vulnerability_intelligence": {
                "cves": vuln_cve_res.scalars().all(),
                "cpes": vuln_cpe_res.scalars().all(),
                "records": vuln_rec_res.scalars().all(),
                "risk_profiles": vuln_prof_res.scalars().all(),
                "evidence": vuln_ev_res.scalars().all(),
                "references": vuln_ref_res.scalars().all()
            }
        }
