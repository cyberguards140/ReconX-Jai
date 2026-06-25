class GraphVisualization:
    @staticmethod
    def format_for_d3(nodes: list, edges: list) -> dict:
        d3_nodes = [
            {"id": n["node_id"], "group": n["node_type"], "label": n["label"]} for n in nodes
        ]
        d3_edges = [
            {"source": e["source"], "target": e["target"], "value": 1, "type": e["type"]}
            for e in edges
        ]
        return {"nodes": d3_nodes, "links": d3_edges}
