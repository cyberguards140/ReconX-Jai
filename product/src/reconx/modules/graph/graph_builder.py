class GraphBuilder:
    @staticmethod
    def build_node(node_id: str, node_type: str, label: str, properties: dict = None) -> dict:
        return {"node_id": node_id, "node_type": node_type, "label": label, "properties": properties or {}}

    @staticmethod
    def build_edge(source: str, target: str, edge_type: str, properties: dict = None) -> dict:
        edge_id = f"{source}-{edge_type}-{target}"
        return {"edge_id": edge_id, "source": source, "target": target, "type": edge_type, "properties": properties or {}}
