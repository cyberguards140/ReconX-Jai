from enum import Enum


class NodeLabel(str, Enum):
    # Asset Nodes
    ASSET = "Asset"
    DOMAIN = "Domain"
    SUBDOMAIN = "Subdomain"
    IP = "IP"
    URL = "URL"
    PORT = "Port"
    TECHNOLOGY = "Technology"
    CERTIFICATE = "Certificate"

    # Infrastructure Nodes
    ASN = "ASN"
    ORGANIZATION = "Organization"
    NETBLOCK = "Netblock"
    HOSTING_PROVIDER = "HostingProvider"

    # Threat Nodes
    IOC = "IOC"
    THREAT_ACTOR = "ThreatActor"
    CAMPAIGN = "Campaign"
    MALWARE = "Malware"
    TECHNIQUE = "Technique"
    TACTIC = "Tactic"

    # SOC Nodes
    ALERT = "Alert"
    INCIDENT = "Incident"
    CASE = "Case"
    INVESTIGATION = "Investigation"
    PLAYBOOK = "Playbook"

    # Cloud Nodes
    CLUSTER = "Cluster"
    NAMESPACE = "Namespace"
    WORKLOAD = "Workload"
    CONTAINER = "Container"
    SERVICE = "Service"
    SERVICE_MESH = "ServiceMesh"

    # Executive Nodes
    RISK = "Risk"
    CONTROL = "Control"
    COMPLIANCE_FRAMEWORK = "ComplianceFramework"
    BUSINESS_UNIT = "BusinessUnit"
