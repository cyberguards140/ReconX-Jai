import socket


class DNSResolver:
    """Utility class to perform quick, authoritative lookups internally if needed."""

    @staticmethod
    def resolve_a(domain: str) -> list[str]:
        try:
            _, _, ips = socket.gethostbyname_ex(domain)
            return ips
        except socket.gaierror:
            return []
