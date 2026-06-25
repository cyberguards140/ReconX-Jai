class ContentEnricher:
    """Helper to verify if a port/service is HTTP/HTTPS before scanning."""

    @staticmethod
    def is_web_service(port: int, protocol: str) -> bool:
        return port in [80, 443, 8080, 8443] or "http" in protocol.lower()
