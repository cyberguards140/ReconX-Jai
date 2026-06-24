import re

def parse(line):
    line = line.strip()
    if not line: return None
    # Subfinder prints subdomains on stdout
    # If it looks like a domain (roughly), treat as subdomain
    if re.match(r'^[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', line):
        return {
            "type": "subdomain",
            "value": line,
            "related": []
        }
    return None
