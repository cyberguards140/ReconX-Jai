from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from data.database.models import (
    CMS,
    WAF,
    ADComputer,
    ADDomain,
    ADGroup,
    ADTrustRelationship,
    ADUser,
    AnalyticsAssetProfile,
    AnalyticsRecommendation,
    AssetRelationship,
    AutomationAlert,
    AutomationChangeEvent,
    AutomationJob,
    Certificate,
    CipherSuite,
    CloudAccount,
    CloudContainerImage,
    CloudKubernetesCluster,
    CloudPod,
    ContentItem,
    DNSRecord,
    Endpoint,
    EnterpriseAPIKey,
    EnterpriseAuditLog,
    EnterpriseTenant,
    EnterpriseUser,
    Framework,
    GraphEdge,
    GraphNode,
    HTTPHeader,
    OSINTEmail,
    OSINTOrganization,
    OSINTProfile,
    OSINTUsername,
    Port,
    ReportEvidence,
    ReportRecord,
    Route,
    Service,
    SMBGroup,
    SMBHost,
    SMBShare,
    SMBUser,
    Technology,
    TLSConfiguration,
    TrafficCommunication,
    TrafficFlow,
    TrafficProtocol,
    VirtualHost,
    VulnCVE,
    VulnRecord,
    VulnRiskProfile,
)
from data.database.repositories.asset import asset_repo
from data.database.repositories.finding import finding_repo
from recon.modules.graph.visualization import GraphVisualization
from recon.modules.reporting.evidence_manager import EvidenceManager
from recon.modules.reporting.export_engine import ExportEngine
from recon.services.health import HealthService
from recon.services.intelligence.risk_scoring import RiskScoring
from reporting.trend_analyzer import TrendAnalyzer


class DashboardService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_metrics(self) -> dict[str, Any]:
        assets = await asset_repo.get_multi(self.db)
        findings = await finding_repo.get_multi(self.db)

        # Calculate Port/Service/Route density
        port_result = await self.db.execute(select(Port))
        ports = port_result.scalars().all()

        service_result = await self.db.execute(select(Service))
        services = service_result.scalars().all()

        route_result = await self.db.execute(select(Route))
        routes = route_result.scalars().all()

        # Web Fingerprinting Aggregation
        tech_result = await self.db.execute(select(Technology))
        technologies = tech_result.scalars().all()

        cms_result = await self.db.execute(select(CMS))
        cms_records = cms_result.scalars().all()

        fw_result = await self.db.execute(select(Framework))
        frameworks = fw_result.scalars().all()

        waf_result = await self.db.execute(select(WAF))
        wafs = waf_result.scalars().all()

        # Content Discovery Aggregation
        content_res = await self.db.execute(select(ContentItem))
        content_items = content_res.scalars().all()

        endpoint_res = await self.db.execute(select(Endpoint))
        endpoints = endpoint_res.scalars().all()

        vhost_res = await self.db.execute(select(VirtualHost))
        vhosts = vhost_res.scalars().all()

        # Web Assessment Aggregation
        cert_res = await self.db.execute(select(Certificate))
        certificates = cert_res.scalars().all()

        tls_res = await self.db.execute(select(TLSConfiguration))
        tls_configs = tls_res.scalars().all()

        cipher_res = await self.db.execute(select(CipherSuite))
        cipher_suites = cipher_res.scalars().all()

        hdr_res = await self.db.execute(select(HTTPHeader))
        headers = hdr_res.scalars().all()

        # SMB Aggregation
        smb_host_res = await self.db.execute(select(SMBHost))
        smb_hosts = smb_host_res.scalars().all()

        smb_share_res = await self.db.execute(select(SMBShare))
        smb_shares = smb_share_res.scalars().all()

        smb_user_res = await self.db.execute(select(SMBUser))
        smb_users = smb_user_res.scalars().all()

        smb_group_res = await self.db.execute(select(SMBGroup))
        smb_groups = smb_group_res.scalars().all()

        # Active Directory Aggregation
        ad_dom_res = await self.db.execute(select(ADDomain))
        ad_domains = ad_dom_res.scalars().all()

        ad_user_res = await self.db.execute(select(ADUser))
        ad_users = ad_user_res.scalars().all()

        ad_group_res = await self.db.execute(select(ADGroup))
        ad_groups = ad_group_res.scalars().all()

        ad_comp_res = await self.db.execute(select(ADComputer))
        ad_computers = ad_comp_res.scalars().all()

        ad_trust_res = await self.db.execute(select(ADTrustRelationship))
        ad_trusts = ad_trust_res.scalars().all()

        # OSINT Aggregation
        osint_org_res = await self.db.execute(select(OSINTOrganization))
        osint_orgs = osint_org_res.scalars().all()

        osint_email_res = await self.db.execute(select(OSINTEmail))
        osint_emails = osint_email_res.scalars().all()

        osint_uname_res = await self.db.execute(select(OSINTUsername))
        osint_unames = osint_uname_res.scalars().all()

        osint_prof_res = await self.db.execute(select(OSINTProfile))
        osint_profs = osint_prof_res.scalars().all()

        # Traffic Aggregation
        traffic_flow_res = await self.db.execute(select(TrafficFlow))
        traffic_flows = traffic_flow_res.scalars().all()

        traffic_proto_res = await self.db.execute(select(TrafficProtocol))
        traffic_protos = traffic_proto_res.scalars().all()

        traffic_comm_res = await self.db.execute(select(TrafficCommunication))
        traffic_comms = traffic_comm_res.scalars().all()

        # Cloud & Container Aggregation
        cloud_acc_res = await self.db.execute(select(CloudAccount))
        cloud_accs = cloud_acc_res.scalars().all()

        cloud_k8s_res = await self.db.execute(select(CloudKubernetesCluster))
        cloud_k8s = cloud_k8s_res.scalars().all()

        cloud_pod_res = await self.db.execute(select(CloudPod))
        cloud_pods = cloud_pod_res.scalars().all()

        cloud_img_res = await self.db.execute(select(CloudContainerImage))
        cloud_imgs = cloud_img_res.scalars().all()

        # Vulnerability Aggregation
        vuln_cve_res = await self.db.execute(select(VulnCVE))
        vuln_cves = vuln_cve_res.scalars().all()

        vuln_rec_res = await self.db.execute(select(VulnRecord))
        vuln_recs = vuln_rec_res.scalars().all()

        vuln_prof_res = await self.db.execute(
            select(VulnRiskProfile).order_by(VulnRiskProfile.risk_score.desc()).limit(10)
        )
        top_risk_profiles = vuln_prof_res.scalars().all()

        # DNS Intelligence Aggregation
        dns_result = await self.db.execute(select(DNSRecord))
        dns_records = dns_result.scalars().all()

        rel_result = await self.db.execute(select(AssetRelationship))
        relationships = rel_result.scalars().all()

        f_dicts = [
            {
                "severity": f.severity.name if hasattr(f.severity, "name") else f.severity,
                "asset_value": getattr(f, "asset_value", "Unknown"),
            }
            for f in findings
        ]
        risk_score = RiskScoring.calculate_project_score(f_dicts)

        critical_count = len(
            [f for f in f_dicts if f["severity"] == "CRITICAL" or f["severity"] == "critical"]
        )
        high_count = len([f for f in f_dicts if f["severity"] == "HIGH" or f["severity"] == "high"])
        medium_count = len(
            [f for f in f_dicts if f["severity"] == "MEDIUM" or f["severity"] == "medium"]
        )
        low_count = len([f for f in f_dicts if f["severity"] == "LOW" or f["severity"] == "low"])
        info_count = len([f for f in f_dicts if f["severity"] == "INFO" or f["severity"] == "info"])

        # Top Services Aggregation
        service_counts = {}
        for svc in services:
            service_counts[svc.service] = service_counts.get(svc.service, 0) + 1
        top_services = dict(
            sorted(service_counts.items(), key=lambda item: item[1], reverse=True)[:5]
        )

        # Tech Aggregations
        tech_counts = {}
        for t in technologies:
            tech_counts[t.technology] = tech_counts.get(t.technology, 0) + 1
        top_technologies = dict(
            sorted(tech_counts.items(), key=lambda item: item[1], reverse=True)[:5]
        )

        cms_inventory = list(set([c.cms for c in cms_records]))
        fw_inventory = list(set([f.framework for f in frameworks]))
        waf_inventory = list(set([w.vendor for w in wafs]))

        # DNS Counts
        dns_counts = {}
        for rec in dns_records:
            dns_counts[rec.record_type] = dns_counts.get(rec.record_type, 0) + 1

        # Fake trend for demonstration
        trend = TrendAnalyzer.compare_scans(
            {"assets": assets, "findings": findings, "risk_score": risk_score},
            {"assets": [], "findings": [], "risk_score": 0},
        )

        subdomains = [a for a in assets if a.asset_type == "subdomain"]
        resolved_subdomains = len([s for s in subdomains if s.is_resolved])
        unresolved_subdomains = len(subdomains) - resolved_subdomains

        # Sources Aggregation
        source_counts = {}
        for s in subdomains:
            if s.sources:
                for src in s.sources:
                    source_counts[src] = source_counts.get(src, 0) + 1
            elif s.source:
                source_counts[s.source] = source_counts.get(s.source, 0) + 1

        top_sources = dict(
            sorted(source_counts.items(), key=lambda item: item[1], reverse=True)[:5]
        )

        # Content Aggregations
        status_counts = {}
        for c in content_items:
            status_counts[c.status_code] = status_counts.get(c.status_code, 0) + 1

        # Graph Intelligence Aggregation
        graph_nodes_res = await self.db.execute(select(GraphNode))
        graph_nodes = graph_nodes_res.scalars().all()

        graph_edges_res = await self.db.execute(select(GraphEdge))
        graph_edges = graph_edges_res.scalars().all()

        # Analytics Aggregation
        analytics_recs = (await self.db.execute(select(AnalyticsRecommendation))).scalars().all()
        analytics_profiles = (
            (
                await self.db.execute(
                    select(AnalyticsAssetProfile)
                    .order_by(AnalyticsAssetProfile.risk_score.desc())
                    .limit(10)
                )
            )
            .scalars()
            .all()
        )

        # Automation Aggregation
        pending_jobs = len(
            (await self.db.execute(select(AutomationJob).where(AutomationJob.status == "Pending")))
            .scalars()
            .all()
        )
        recent_alerts = (
            (
                await self.db.execute(
                    select(AutomationAlert).order_by(AutomationAlert.timestamp.desc()).limit(5)
                )
            )
            .scalars()
            .all()
        )
        recent_changes = (
            (
                await self.db.execute(
                    select(AutomationChangeEvent)
                    .order_by(AutomationChangeEvent.timestamp.desc())
                    .limit(5)
                )
            )
            .scalars()
            .all()
        )

        # Enterprise Aggregation
        tenant_count = len((await self.db.execute(select(EnterpriseTenant))).scalars().all())
        user_count = len((await self.db.execute(select(EnterpriseUser))).scalars().all())
        api_keys_active = len(
            (
                await self.db.execute(
                    select(EnterpriseAPIKey).where(EnterpriseAPIKey.status == "Active")
                )
            )
            .scalars()
            .all()
        )
        recent_audits = (
            (
                await self.db.execute(
                    select(EnterpriseAuditLog)
                    .order_by(EnterpriseAuditLog.timestamp.desc())
                    .limit(5)
                )
            )
            .scalars()
            .all()
        )

        # Production System Health
        sys_health = HealthService.check_health()

        return {
            "total_assets": len(assets),
            "live_hosts": len([a for a in assets if a.asset_type in ["ip"]]),
            "domains": len([a for a in assets if a.asset_type == "domain"]),
            "subdomains": len(subdomains),
            "resolved_subdomains": resolved_subdomains,
            "unresolved_subdomains": unresolved_subdomains,
            "top_discovery_sources": top_sources,
            "infrastructure": {
                "asns": len([a for a in assets if a.asset_type == "asn"]),
                "netblocks": len([a for a in assets if a.asset_type == "netblock"]),
            },
            "total_ports": len(ports),
            "total_routes": len(routes),
            "top_services": top_services,
            "top_technologies": top_technologies,
            "cms_inventory": cms_inventory,
            "framework_inventory": fw_inventory,
            "waf_inventory": waf_inventory,
            "content_inventory": {
                "total_paths": len(content_items),
                "total_endpoints": len(endpoints),
                "total_vhosts": len(vhosts),
            },
            "response_distribution": status_counts,
            "tls_inventory": {
                "certificates": len(certificates),
                "tls_configs": len(tls_configs),
                "cipher_suites": len(cipher_suites),
            },
            "security_headers": len([h for h in headers if h.is_security]),
            "smb_inventory": {
                "total_hosts": len(smb_hosts),
                "total_shares": len(smb_shares),
                "total_users": len(smb_users),
                "total_groups": len(smb_groups),
            },
            "ad_inventory": {
                "total_domains": len(ad_domains),
                "total_users": len(ad_users),
                "total_groups": len(ad_groups),
                "total_computers": len(ad_computers),
                "total_trusts": len(ad_trusts),
            },
            "osint_inventory": {
                "total_organizations": len(osint_orgs),
                "total_emails": len(osint_emails),
                "total_usernames": len(osint_unames),
                "total_profiles": len(osint_profs),
            },
            "traffic_overview": {
                "total_flows": len(traffic_flows),
                "protocols_detected": len(traffic_protos),
                "mapped_communications": len(traffic_comms),
            },
            "cloud_inventory": {
                "total_accounts": len(cloud_accs),
                "kubernetes_clusters": len(cloud_k8s),
                "active_pods": len(cloud_pods),
                "container_images": len(cloud_imgs),
            },
            "vulnerability_overview": {
                "total_cves_tracked": len(vuln_cves),
                "total_vuln_records": len(vuln_recs),
                "highest_risk_assets": [
                    {"asset_id": p.asset_id, "score": p.risk_score} for p in top_risk_profiles
                ],
            },
            "dns_stats": dns_counts,
            "relationships_mapped": len(relationships),
            "risk_score": risk_score,
            "reports": {
                "generated": [
                    r.title for r in (await self.db.execute(select(ReportRecord))).scalars().all()
                ],
                "evidence_files": len(
                    (await self.db.execute(select(ReportEvidence))).scalars().all()
                ),
            },
            "graph_intelligence": {
                "total_nodes": len(graph_nodes),
                "total_edges": len(graph_edges),
            },
            "analytics": {
                "top_recommendations": [
                    {"title": r.title, "impact": r.impact} for r in analytics_recs
                ],
                "top_assets": [
                    {"asset_id": p.asset_id, "score": p.risk_score} for p in analytics_profiles
                ],
            },
            "automation": {
                "pending_jobs": pending_jobs,
                "recent_alerts": [
                    {"message": a.message, "severity": a.severity} for a in recent_alerts
                ],
                "recent_changes": [
                    {"type": c.change_type, "entity": c.entity_type} for c in recent_changes
                ],
            },
            "enterprise": {
                "total_tenants": tenant_count,
                "total_users": user_count,
                "active_api_keys": api_keys_active,
                "recent_audits": [
                    {"user_id": a.user_id, "action": a.action} for a in recent_audits
                ],
            },
            "system_health": sys_health,
            "critical_findings": critical_count,
            "high_findings": high_count,
            "medium_findings": medium_count,
            "low_findings": low_count,
            "info_findings": info_count,
            "trends": trend,
        }

    async def export_dashboard_json(self) -> str:
        data = await self.get_dashboard_summary()
        return ExportEngine.export_json(data)

    async def export_dashboard_csv(self) -> str:
        data = await self.get_dashboard_summary()
        # Flat mock CSV for metrics
        headers = ["metric", "value"]
        rows = [
            ["total_assets", data["total_assets"]],
            ["total_findings", data["total_findings"]],
            ["risk_score", data["risk_score"]],
        ]
        return ExportEngine.export_csv(headers, rows)

    async def get_evidence(self, finding_id: str) -> str:
        manager = EvidenceManager()
        return manager.get_evidence(finding_id)

    async def get_attack_surface_graph(self) -> dict:
        nodes = (await self.db.execute(select(GraphNode))).scalars().all()
        edges = (await self.db.execute(select(GraphEdge))).scalars().all()

        nodes_list = [
            {"node_id": n.node_id, "node_type": n.node_type, "label": n.label} for n in nodes
        ]
        edges_list = [
            {"source": e.source_node_id, "target": e.target_node_id, "type": e.edge_type}
            for e in edges
        ]

        return GraphVisualization.format_for_d3(nodes_list, edges_list)
