import os
import sys
import logging
from core.registry_db import SessionLocal, Category, Tool, ToolArgument, ToolDependency

# Setup logging
if not os.path.exists('logs'):
    os.makedirs('logs')
reg_logger = logging.getLogger("registry")
reg_logger.setLevel(logging.INFO)
fh = logging.FileHandler('logs/tool_registry.log')
fh.setFormatter(logging.Formatter('%(asctime)s - %(message)s'))
reg_logger.addHandler(fh)

def seed_registry():
    db = SessionLocal()

    # Avoid duplicate seeds
    if db.query(Category).first() is not None:
        db.close()
        return

    # Seed Categories
    categories = [
        {"id": "recon", "name": "Recon & Info", "order": 1},
        {"id": "vuln", "name": "Vuln Scan", "order": 2},
        {"id": "web", "name": "Web Enum", "order": 3},
        {"id": "cloud", "name": "Cloud", "order": 4}
    ]
    for c in categories:
        db.add(Category(**c))
    
    # Seed Tools
    tools_data = {
        "recon": ["Subfinder", "Amass", "Assetfinder", "Findomain", "Chaos", "DNSX", "Naabu", "Masscan", "Nmap", "Httpx", "Katana", "Waybackurls", "GAU", "Hakrawler", "TheHarvester", "Shodan", "Whois", "ASN Lookup", "Reverse DNS"],
        "vuln": ["Nuclei", "Nikto", "OpenVAS", "Nessus", "SSLScan", "TestSSL"],
        "web": ["Dirsearch", "Feroxbuster", "Gobuster", "FFUF", "Katana", "LinkFinder", "SecretFinder", "JSFinder"],
        "cloud": ["AWS Enumeration", "Azure Enumeration", "GCP Enumeration", "S3 Scanner", "Cloud Asset Discovery"]
    }
    
    seen_tools = set()
    for cat_id, names in tools_data.items():
        for name in names:
            tool_id = name.lower().replace(" ", "_").replace("&", "").strip()
            if tool_id in seen_tools:
                continue
            seen_tools.add(tool_id)
            
            db.add(Tool(
                id=tool_id,
                name=name,
                category_id=cat_id,
                description=f"{name} tool",
                binary=tool_id,
                enabled=True,
                tags=[cat_id]
            ))

    db.commit()

    # Explicit Nmap Arguments
    nmap_args = [
        {"flag": "-sS", "type": "toggle"},
        {"flag": "-sT", "type": "toggle"},
        {"flag": "-sU", "type": "toggle"},
        {"flag": "-sV", "type": "toggle"},
        {"flag": "-O", "type": "toggle"},
        {"flag": "-A", "type": "toggle"},
        {"flag": "-Pn", "type": "toggle"},
        {"flag": "-sC", "type": "toggle"},
        {"flag": "--script", "type": "textbox"},
        {"flag": "-v", "type": "toggle"},
        {"flag": "-vv", "type": "toggle"},
        {"flag": "-vvv", "type": "toggle"},
        {"flag": "-p", "type": "textbox"},
        {"flag": "--top-ports", "type": "number"},
        {"flag": "-oN", "type": "textbox"},
        {"flag": "-oX", "type": "textbox"},
        {"flag": "-oG", "type": "textbox"}
    ]
    for arg in nmap_args:
        db.add(ToolArgument(
            tool_id="nmap",
            flag=arg['flag'],
            type=arg['type']
        ))

    # Nmap Dependencies
    deps = [
        {"tool_id": "nmap", "dep_type": "binary", "name": "nmap"},
        {"tool_id": "nmap", "dep_type": "python", "name": "python3"},
        {"tool_id": "nmap", "dep_type": "pip", "name": "python-nmap"},
        {"tool_id": "nmap", "dep_type": "system", "name": "libpcap"}
    ]
    for d in deps:
        db.add(ToolDependency(**d))

    db.commit()
    db.close()
    
    reg_logger.info("Registry seeded with default categories and tools.")

if __name__ == "__main__":
    seed_registry()
