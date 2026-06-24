class GraphStorage:
    def __init__(self):
        self.nodes = {}
        self.edges = {}
        
    def add_node(self, node: dict):
        self.nodes[node["node_id"]] = node
        
    def add_edge(self, edge: dict):
        self.edges[edge["edge_id"]] = edge
        
    def get_neighbors(self, node_id: str) -> list:
        neighbors = []
        for edge in self.edges.values():
            if edge["source"] == node_id:
                neighbors.append(edge["target"])
        return neighbors
