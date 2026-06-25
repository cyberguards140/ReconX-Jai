from .asset_manager import AssetManager


class ResultRouter:
    def __init__(self):
        self.asset_manager = AssetManager()

    def route(self, normalized_data):
        if "asset_type" in normalized_data and "value" in normalized_data:
            return self.asset_manager.create_asset(
                normalized_data["asset_type"], normalized_data["value"]
            )
        return None
