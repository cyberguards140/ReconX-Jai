from recon.modules.asm_core.schema import UnifiedAsset


class ThreatLinker:
    """
    Conceptually maps assets to known threat patterns and tags.
    """

    def __init__(self):
        pass

    def get_threat_tags(self, asset: UnifiedAsset) -> list[str]:
        # Conceptual linking logic
        tags = []
        if asset.asset_type == "service":
            tech = asset.metadata.get("tech", [])
            if "wordpress" in tech or "joomla" in tech:
                tags.append("CMS Exposure")

        if asset.confidence < 30.0:
            tags.append("Low Confidence Discovery")

        return tags
