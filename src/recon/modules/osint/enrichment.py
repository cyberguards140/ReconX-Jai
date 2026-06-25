class OSINTEnricher:
    """Helper to verify target types before sending to specific OSINT tools."""

    @staticmethod
    def is_email(target: str) -> bool:
        return "@" in target and "." in target

    @staticmethod
    def is_username(target: str) -> bool:
        return "@" not in target and "." not in target
