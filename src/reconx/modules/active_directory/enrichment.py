class ADEnricher:
    """Helper to verify if a port/service is AD related before scanning."""
    
    @staticmethod
    def is_ad_service(port: int) -> bool:
        return port in [88, 389, 636, 3268, 3269]
