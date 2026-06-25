from reconx.modules.asm_core.schema import UnifiedAsset
from reconx.modules.visual_intel.schema import TopologyZone, VisualCluster


class TopologyBuilder:
    """
    Groups assets into conceptual zones and clusters.
    """

    def __init__(self):
        pass

    def build_zones(self, assets: list[UnifiedAsset]) -> list[TopologyZone]:
        # Conceptual zone grouping
        internet_zone = TopologyZone(
            zone_name="Internet Zone", description="Publicly reachable assets"
        )
        internal_zone = TopologyZone(
            zone_name="Internal Exposure Layer", description="Internal assets"
        )

        for asset in assets:
            if asset.asset_type in ["domain", "url"]:
                internet_zone.member_asset_ids.append(asset.asset_id)
            elif asset.asset_type == "ip":
                internal_zone.member_asset_ids.append(asset.asset_id)

        return [internet_zone, internal_zone]

    def build_clusters(self, assets: list[UnifiedAsset]) -> list[VisualCluster]:
        # Conceptual clustering
        web_cluster = VisualCluster(cluster_id="web_app_01", cluster_type="Web Application Cluster")
        for asset in assets:
            if asset.asset_type == "service" and "http" in str(asset.value).lower():
                web_cluster.member_asset_ids.append(asset.asset_id)

        return [web_cluster]
