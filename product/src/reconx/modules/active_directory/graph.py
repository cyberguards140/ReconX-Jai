class ADGraphBuilder:
    """Handles mapping AD computers to network assets."""
    @staticmethod
    def map_to_asset(hostname: str, ip: str) -> dict:
        return {"hostname": hostname, "ip": ip, "relationship": "resolves_to"}
