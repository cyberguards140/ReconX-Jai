class NormalizationEngine:
    def normalize(self, raw_asset):
        # Ensure schema compliance
        return {"asset_type": raw_asset.get("type"), "value": raw_asset.get("value")}
