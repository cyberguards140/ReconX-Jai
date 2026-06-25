class PacketCorrelation:
    """Handles mapping Traffic flows back to Stage 3 Assets."""

    @staticmethod
    def map_flow_to_asset(flow_ip: str, asset_ip: str) -> dict:
        return {
            "source": flow_ip,
            "target": asset_ip,
            "type": "originates_from" if flow_ip == asset_ip else "communicates_with",
        }
