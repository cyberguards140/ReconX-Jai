import json
import os

tools = [
  {"id": "nmap", "name": "Nmap", "category": "recon_info", "binary": "nmap", "enabled": True},
  {"id": "masscan", "name": "Masscan", "category": "recon_info", "binary": "masscan", "enabled": True},
  {"id": "rustscan", "name": "Rustscan", "category": "recon_info", "binary": "rustscan", "enabled": True},
  {"id": "amass", "name": "Amass", "category": "recon_info", "binary": "amass", "enabled": True},
  {"id": "subfinder", "name": "Subfinder", "category": "recon_info", "binary": "subfinder", "enabled": True},
  {"id": "assetfinder", "name": "Assetfinder", "category": "recon_info", "binary": "assetfinder", "enabled": True},
  {"id": "findomain", "name": "Findomain", "category": "recon_info", "binary": "findomain", "enabled": True},
  {"id": "chaos", "name": "Chaos", "category": "recon_info", "binary": "chaos", "enabled": True},
  {"id": "asnmap", "name": "ASNMap", "category": "recon_info", "binary": "asnmap", "enabled": True},
  {"id": "whois", "name": "Whois", "category": "recon_info", "binary": "whois", "enabled": True},
  {"id": "dnsx", "name": "DNSX", "category": "recon_info", "binary": "dnsx", "enabled": True},
  {"id": "httpx", "name": "Httpx", "category": "recon_info", "binary": "httpx", "enabled": True},
  {"id": "naabu", "name": "Naabu", "category": "recon_info", "binary": "naabu", "enabled": True},
  {"id": "katana", "name": "Katana", "category": "web", "binary": "katana", "enabled": True},
  {"id": "hakrawler", "name": "Hakrawler", "category": "web", "binary": "hakrawler", "enabled": True},
  {"id": "gau", "name": "GAU", "category": "web", "binary": "gau", "enabled": True},
  {"id": "waybackurls", "name": "Waybackurls", "category": "web", "binary": "waybackurls", "enabled": True},
  {"id": "whatweb", "name": "WhatWeb", "category": "web", "binary": "whatweb", "enabled": True},
  {"id": "wappalyzer", "name": "Wappalyzer", "category": "web", "binary": "wappalyzer", "enabled": True},
  {"id": "aquatone-web", "name": "Aquatone", "category": "web", "binary": "aquatone", "enabled": True},
  {"id": "gowitness-web", "name": "Gowitness", "category": "web", "binary": "gowitness", "enabled": True},
  {"id": "nuclei", "name": "Nuclei", "category": "vulnerability", "binary": "nuclei", "enabled": True},
  {"id": "nikto", "name": "Nikto", "category": "vulnerability", "binary": "nikto", "enabled": True},
  {"id": "sslscan", "name": "SSLScan", "category": "vulnerability", "binary": "sslscan", "enabled": True},
  {"id": "testssl", "name": "TestSSL", "category": "vulnerability", "binary": "testssl", "enabled": True},
  {"id": "dalfox", "name": "Dalfox", "category": "vulnerability", "binary": "dalfox", "enabled": True},
  {"id": "cloudenum", "name": "CloudEnum", "category": "cloud", "binary": "cloudenum", "enabled": True},
  {"id": "s3scanner", "name": "S3Scanner", "category": "cloud", "binary": "s3scanner", "enabled": True},
  {"id": "aws-cli", "name": "AWS CLI", "category": "cloud", "binary": "aws", "enabled": True},
  {"id": "azure-cli", "name": "Azure CLI", "category": "cloud", "binary": "az", "enabled": True},
  {"id": "gcloud-cli", "name": "GCloud CLI", "category": "cloud", "binary": "gcloud", "enabled": True},
  {"id": "shodan", "name": "Shodan", "category": "osint", "binary": "shodan", "enabled": True},
  {"id": "theharvester", "name": "TheHarvester", "category": "osint", "binary": "theHarvester", "enabled": True},
  {"id": "phonebook", "name": "Phonebook", "category": "osint", "binary": "phonebook", "enabled": True},
  {"id": "crtsh", "name": "CRTSH", "category": "osint", "binary": "crtsh", "enabled": True},
  {"id": "securitytrails", "name": "SecurityTrails", "category": "osint", "binary": "securitytrails", "enabled": True},
  {"id": "aquatone", "name": "Aquatone", "category": "screenshot", "binary": "aquatone", "enabled": True},
  {"id": "gowitness", "name": "Gowitness", "category": "screenshot", "binary": "gowitness", "enabled": True},
  {"id": "witnessweb", "name": "WitnessWeb", "category": "screenshot", "binary": "witnessweb", "enabled": True},
  {"id": "trufflehog", "name": "TruffleHog", "category": "secrets", "binary": "trufflehog", "enabled": True},
  {"id": "gitleaks", "name": "GitLeaks", "category": "secrets", "binary": "gitleaks", "enabled": True}
]

metadata = []
dependencies = []
outputs = []
adapters = []

for t in tools:
    tid = t['id']
    bin_name = t['binary']
    
    metadata.append({
        "id": tid,
        "display_name": t['name'],
        "category": t['category'],
        "binary": bin_name,
        "version_command": f"{bin_name} --version" if bin_name not in ['theHarvester', 'gowitness', 'amass', 'subfinder', 'nuclei'] else f"{bin_name} -version",
        "supports_streaming": True,
        "supports_json": tid in ['subfinder', 'amass', 'nuclei', 'httpx', 'katana', 'dnsx', 'naabu', 'shodan', 'aws-cli', 'gcloud-cli'],
        "supports_xml": tid in ['nmap', 'masscan'],
        "requires_api_key": tid in ['shodan', 'subfinder', 'amass', 'github-endpoints', 'securitytrails'],
        "supports_projects": True
    })
    
    install_method = "apt"
    if tid in ['subfinder', 'amass', 'assetfinder', 'chaos', 'asnmap', 'dnsx', 'httpx', 'naabu', 'katana', 'hakrawler', 'gau', 'gowitness', 'gowitness-web', 'nuclei', 's3scanner']:
        install_method = "go install"
    elif tid in ['theharvester', 'cloudenum']:
        install_method = "pip"
    
    dependencies.append({
        "tool": tid,
        "binary": bin_name,
        "required": True,
        "install_method": install_method
    })
    
    formats = ["txt"]
    if tid in ['nmap', 'masscan']:
        formats.append("xml")
    if tid in ['subfinder', 'amass', 'nuclei', 'httpx', 'katana', 'dnsx', 'naabu', 'shodan', 'aws-cli', 'gcloud-cli']:
        formats.append("json")
        
    outputs.append({
        "tool": tid,
        "formats": formats
    })
    
    adapters.append({
        "tool": tid,
        "adapter": "shell_adapter"
    })

def write_json(filename, data):
    with open(f"/home/kali/ReconX/registry/{filename}", "w") as f:
        json.dump(data, f, indent=2)

write_json("tool_metadata.json", metadata)
write_json("dependencies.json", dependencies)
write_json("outputs.json", outputs)
write_json("adapters.json", adapters)
print("Done!")
