import pytest
from reconx.modules.graph.graph_builder import GraphBuilder
from reconx.modules.graph.relationship_mapper import RelationshipMapper
from reconx.modules.graph.visualization import GraphVisualization
from reconx.modules.graph.exports import GraphExporter
from reconx.services.relationship_engine import RelationshipEngine
from reconx.services.graph_storage import GraphStorage

def test_graph_builder_node():
    node = GraphBuilder.build_node("n1", "Domain", "example.com")
    assert node["node_id"] == "n1"
    assert node["node_type"] == "Domain"
    assert node["label"] == "example.com"

def test_graph_builder_edge():
    edge = GraphBuilder.build_edge("n1", "n2", "RESOLVES_TO")
    assert edge["source"] == "n1"
    assert edge["target"] == "n2"
    assert edge["type"] == "RESOLVES_TO"
    assert "RESOLVES_TO" in edge["edge_id"]

def test_relationship_engine_ontology():
    edges = RelationshipEngine.get_valid_edges("Domain")
    assert "RESOLVES_TO" in edges
    assert "HOSTS" not in edges

def test_relationship_mapper_ad():
    users = [{"id": "u1", "groups": ["g1", "g2"]}]
    edges = RelationshipMapper.map_ad_relationships(users, [])
    assert len(edges) == 2
    assert edges[0]["type"] == "MEMBER_OF"

def test_graph_storage():
    storage = GraphStorage()
    storage.add_node(GraphBuilder.build_node("n1", "Domain", "example.com"))
    storage.add_node(GraphBuilder.build_node("n2", "IP", "1.2.3.4"))
    storage.add_edge(GraphBuilder.build_edge("n1", "n2", "RESOLVES_TO"))
    
    neighbors = storage.get_neighbors("n1")
    assert "n2" in neighbors

def test_visualization_d3():
    nodes = [{"node_id": "n1", "node_type": "Domain", "label": "example.com"}]
    edges = [{"source": "n1", "target": "n2", "type": "RESOLVES_TO"}]
    data = GraphVisualization.format_for_d3(nodes, edges)
    
    assert data["nodes"][0]["id"] == "n1"
    assert data["links"][0]["source"] == "n1"

def test_graph_exporter_graphml():
    nodes = [{"node_id": "n1", "node_type": "Domain", "label": "example.com"}]
    edges = [{"edge_id": "e1", "source": "n1", "target": "n2", "type": "RESOLVES_TO"}]
    graphml = GraphExporter.to_graphml(nodes, edges)
    
    assert '<?xml version="1.0" encoding="UTF-8"?>' in graphml
    assert '<node id="n1"/>' in graphml
    assert '<edge id="e1" source="n1" target="n2"/>' in graphml
