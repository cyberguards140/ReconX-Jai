from graph.graph_engine import GraphEngine
from graph.relationships import RelationshipTypes

class AssetCorrelationEngine:
    @staticmethod
    def correlate_dns(project_id, domain, resolved_ip):
        # Auto-link Domain to IP
        dom_id = GraphEngine.add_entity(project_id, "Domain", domain)
        ip_id = GraphEngine.add_entity(project_id, "IP", resolved_ip)
        GraphEngine.add_relationship(project_id, dom_id, ip_id, RelationshipTypes.RESOLVES_TO)
        
    @staticmethod
    def correlate_technology(project_id, asset_val, asset_type, tech_name):
        a_id = GraphEngine.add_entity(project_id, asset_type, asset_val)
        t_id = GraphEngine.add_entity(project_id, "Technology", tech_name)
        GraphEngine.add_relationship(project_id, a_id, t_id, RelationshipTypes.USES)
