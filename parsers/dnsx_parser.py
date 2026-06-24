import re

def parse(line):
    line = line.strip()
    if not line: return None
    # Very basic DNSX output: api.example.com [1.2.3.4]
    match = re.search(r'^(\S+)\s+\[([0-9\.]+)\]', line)
    if match:
        domain = match.group(1)
        ip = match.group(2)
        return {
            "type": "subdomain",
            "value": domain,
            "related": [{"type": "ip", "value": ip, "relation": "resolves_to"}]
        }
    return None
