import re


def parse(line):
    line = line.strip()
    if not line:
        return None
    # Basic HTTPX output: https://api.example.com [200] [Apache]
    match = re.search(r"^(http[s]?://\S+)", line)
    if match:
        url = match.group(1)
        related = []
        tech_match = re.search(r"\[([^\]]+)\]", line[len(url) :])
        if tech_match:
            techs = tech_match.group(1).split(",")
            for t in techs:
                t_clean = t.strip()
                if t_clean.isdigit():
                    continue

                # Basic classification matrix
                category = "technology"
                t_lower = t_clean.lower()
                if any(waf in t_lower for waf in ["cloudflare", "incapsula", "akamai", "aws waf"]):
                    category = "waf"
                elif any(cms in t_lower for cms in ["wordpress", "drupal", "joomla", "ghost"]):
                    category = "cms"
                elif any(lang in t_lower for lang in ["php", "python", "ruby", "java", "node.js"]):
                    category = "language"
                elif any(server in t_lower for server in ["nginx", "apache", "iis", "litespeed"]):
                    category = "web_server"

                related.append({"type": category, "value": t_clean, "relation": "uses"})

        return {"type": "url", "value": url, "related": related}
    return None
