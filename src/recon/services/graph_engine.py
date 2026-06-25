from recon.modules.graph.graph_builder import GraphBuilder
from recon.services.graph_storage import GraphStorage


class GraphEngine:
    def __init__(self):
        self.storage = GraphStorage()

    def sync_asset_to_graph(self, asset_id: str, asset_type: str, label: str):
        node = GraphBuilder.build_node(asset_id, asset_type, label)
        self.storage.add_node(node)

    def sync_relationship_to_graph(self, source_id: str, target_id: str, edge_type: str):
        edge = GraphBuilder.build_edge(source_id, target_id, edge_type)
        self.storage.add_edge(edge)
