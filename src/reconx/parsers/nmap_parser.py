import re


def parse(line):
    # Extremely basic Nmap output parser for MVP
    # Looks for: 443/tcp open  https
    match = re.search(r"^(\d+)/(tcp|udp)\s+open\s+(\S+)", line)
    if match:
        port = match.group(1)
        service = match.group(3)
        return {
            "type": "host",
            # We don't have the target IP extracted simply from a line, but we can assume
            # we are attaching these to the main target via normalization/correlation
            "value": "auto",
            "related": [
                {"type": "port", "value": port, "relation": "has_port"},
                {"type": "service", "value": service, "relation": "runs_service"},
            ],
        }
    return None
