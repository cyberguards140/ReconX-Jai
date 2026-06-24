class ExecutionGraph:
    def __init__(self):
        self.nodes = {}
        self.edges = []
        
    def add_node(self, node_id, data):
        self.nodes[node_id] = data
        
    def add_edge(self, from_node, to_node):
        self.edges.append((from_node, to_node))
