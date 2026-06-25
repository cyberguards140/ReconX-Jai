import re


def parse(line: str) -> dict:
    """
    Parses Nmap output (especially -sV) to extract port, service, and version/banner.
    """
    line = line.strip()

    # Looks for: 443/tcp open  https  nginx 1.18.0
    # Or: 80/tcp  open  http
    match = re.search(r"^(\d+)/(tcp|udp)\s+open\s+([\w\-\.]+)(?:\s+(.*))?", line)
    if match:
        port = match.group(1)
        protocol = match.group(2)
        service = match.group(3)
        version = match.group(4) or ""

        return {
            "type": "host",
            "value": "auto",  # Set by CorrelationEngine
            "related": [
                {"type": "port", "value": port, "protocol": protocol, "relation": "has_port"},
                {
                    "type": "service",
                    "value": service,
                    "banner": version.strip(),
                    "relation": "runs_service",
                },
            ],
        }
    return None
