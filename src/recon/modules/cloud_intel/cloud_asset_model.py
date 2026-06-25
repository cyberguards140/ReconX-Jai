from typing import Any

from recon.modules.cloud_intel.schema import CloudAssetModel


class CloudAssetEngine:
    """
    Manages the abstract representation of cloud resources across providers.
    """

    def __init__(self):
        pass

    def map_cloud_asset(self, raw_data: dict[str, Any]) -> CloudAssetModel:
        """
        Transforms raw cloud asset data into the unified schema.
        """
        return CloudAssetModel(
            cloud_asset_id=raw_data.get("id", "unknown"),
            cloud_provider=raw_data.get("provider", "unknown"),
            asset_type=raw_data.get("type", "unknown"),
            region=raw_data.get("region", "global"),
            exposure_level=raw_data.get("exposure", "Unknown Exposure"),
            linked_assets=raw_data.get("linked", []),
        )
