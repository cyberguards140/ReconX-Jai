import socket

class SubdomainEnricher:
    """Verifies subdomains and attaches resolution info."""
    
    @staticmethod
    def resolve_subdomain(subdomain: str) -> bool:
        try:
            socket.gethostbyname_ex(subdomain)
            return True
        except socket.gaierror:
            return False
