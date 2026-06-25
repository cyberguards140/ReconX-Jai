from typing import Any

from reconx.modules.asm_core.schema import UnifiedAsset
from reconx.modules.visual_intel.asset_screenshot_mapper import AssetScreenshotMapper
from reconx.modules.visual_intel.graph_renderer import GraphRenderer
from reconx.modules.visual_intel.schema import VisualIntelModel
from reconx.modules.visual_intel.topology_builder import TopologyBuilder
from reconx.modules.visual_intel.ui_feed_generator import UIFeedGenerator
from reconx.modules.visual_intel.visual_cache import VisualCache


class VisualizationEngine:
    """
    Orchestrates the visual translation layer.
    """

    def __init__(self):
        self.topology_builder = TopologyBuilder()
        self.graph_renderer = GraphRenderer()
        self.screenshot_mapper = AssetScreenshotMapper()
        self.ui_feed_generator = UIFeedGenerator()
        self.cache = VisualCache()

    def generate_visual_intel(self, asset: UnifiedAsset, risk_score: float) -> VisualIntelModel:
        """
        Creates the visual intelligence object for an asset.
        """
        # Calculate heat
        heat_data = self.graph_renderer.compute_heatmap({asset.asset_id: risk_score})
        heat_level = heat_data[0].heat_level if heat_data else 0

        # In a complete implementation, cluster mapping and layout would happen at a macro level,
        # but here we generate the individual asset's visual struct.
        return VisualIntelModel(
            node_position={"x": 0.0, "y": 0.0},  # Default placeholder
            cluster_id="unassigned",
            visual_tags=["auto_mapped"],
            snapshot_ref="",
            heat_level=heat_level,
        )

    def get_topology_map(self, assets: list[UnifiedAsset]) -> dict[str, Any]:
        """
        Returns a complete structural topology map for UI rendering.
        """
        zones = self.topology_builder.build_zones(assets)
        clusters = self.topology_builder.build_clusters(assets)

        return {
            "zones": [z.model_dump() for z in zones],
            "clusters": [c.model_dump() for c in clusters],
        }
