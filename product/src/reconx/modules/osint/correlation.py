class OSINTCorrelation:
    """Handles building relationship mapping objects for OSINT data."""
    @staticmethod
    def link_org_to_domain(org: str, domain: str) -> dict:
        return {"source": org, "target": domain, "type": "owns"}
