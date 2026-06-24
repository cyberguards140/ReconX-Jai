class CloudCorrelation:
    """Handles mapping Cloud resources back to passive network Assets."""
    @staticmethod
    def map_cloud_ip_to_asset(cloud_resource_id: str, asset_ip: str) -> dict:
        return {"source": cloud_resource_id, "target": asset_ip, "type": "resolves_to"}
