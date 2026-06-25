class SMBEnricher:
    """Helper to verify if a port/service is SMB before scanning."""

    @staticmethod
    def is_smb_service(port: int) -> bool:
        return port in [139, 445]
