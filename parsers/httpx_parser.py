import re

def parse(line):
    line = line.strip()
    if not line: return None
    # Basic HTTPX output: https://api.example.com [200] [Apache]
    match = re.search(r'^(http[s]?://\S+)', line)
    if match:
        url = match.group(1)
        related = []
        tech_match = re.search(r'\[([^\]]+)\]', line[len(url):])
        if tech_match:
            techs = tech_match.group(1).split(',')
            for t in techs:
                if t.strip().isdigit():
                    continue # likely status code
                related.append({"type": "technology", "value": t.strip(), "relation": "uses_tech"})
                
        return {
            "type": "url",
            "value": url,
            "related": related
        }
    return None
