from typing import Any

from reconx.modules.visual_intel.schema import HeatMapSignal


class GraphRenderer:
    """
    Transforms nodes and edges into a visual graph layout structure.
    """

    def __init__(self):
        pass

    def render_layout(
        self, nodes: list[dict[str, Any]], edges: list[dict[str, Any]]
    ) -> dict[str, Any]:
        """
        Abstractly generates positions for nodes (e.g., force-directed layout representation).
        """
        layout = {}
        for i, node in enumerate(nodes):
            # Dummy positioning logic for demonstration
            layout[node.get("id", str(i))] = {"x": i * 10.0, "y": i * 10.0}

        return {"layout_type": "force-directed", "positions": layout}

    def compute_heatmap(self, risk_scores: dict[str, float]) -> list[HeatMapSignal]:
        """
        Translates risk scores to visual heat colors.
        Low risk -> green (0-30)
        Medium risk -> yellow (31-60)
        High risk -> orange (61-89)
        Critical -> red (90-100)
        """
        heatmap = []
        for asset_id, score in risk_scores.items():
            if score >= 90:
                color = "red"
                level = 4
            elif score >= 60:
                color = "orange"
                level = 3
            elif score >= 30:
                color = "yellow"
                level = 2
            else:
                color = "green"
                level = 1

            heatmap.append(HeatMapSignal(asset_id=asset_id, heat_level=level, color_code=color))

        return heatmap
