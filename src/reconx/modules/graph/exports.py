import json


class GraphExporter:
    @staticmethod
    def to_json(nodes: list, edges: list) -> str:
        return json.dumps({"nodes": nodes, "edges": edges}, indent=2)

    @staticmethod
    def to_graphml(nodes: list, edges: list) -> str:
        # Simplified GraphML for validation
        lines = [
            '<?xml version="1.0" encoding="UTF-8"?>',
            '<graphml xmlns="http://graphml.graphdrawing.org/xmlns">',
            '  <graph id="G" edgedefault="directed">',
        ]
        for n in nodes:
            lines.append(f'    <node id="{n["node_id"]}"/>')
        for e in edges:
            lines.append(
                f'    <edge id="{e["edge_id"]}" source="{e["source"]}" target="{e["target"]}"/>'
            )
        lines.append("  </graph>\n</graphml>")
        return "\n".join(lines)
