import json
import os

OUT_DIR = "/home/kali/ReconX/registry/arguments"
os.makedirs(OUT_DIR, exist_ok=True)

# Nmap
nmap = [
    {"flag": "-sS", "name": "SYN Scan", "type": "toggle", "default": False, "required": False},
    {"flag": "-sV", "name": "Version Detection", "type": "toggle", "default": False, "required": False},
    {"flag": "-O", "name": "OS Detection", "type": "toggle", "default": False, "required": False},
    {"flag": "-sC", "name": "Default Scripts", "type": "toggle", "default": False, "required": False},
    {"flag": "-Pn", "name": "Skip Host Discovery", "type": "toggle", "default": False, "required": False},
    {"flag": "-p", "name": "Ports", "type": "text", "default": "", "required": False},
    {"flag": "-T", "name": "Timing", "type": "dropdown", "options": ["0", "1", "2", "3", "4", "5"], "default": "3", "required": False},
    {"flag": "--script", "name": "NSE Scripts", "type": "text", "default": "", "required": False},
    {"flag": "-oN", "name": "Normal Output", "type": "text", "default": "", "required": False},
    {"flag": "-oX", "name": "XML Output", "type": "text", "default": "", "required": False},
    {"flag": "-oG", "name": "Grepable Output", "type": "text", "default": "", "required": False},
    {"flag": "-v", "name": "Verbosity", "type": "toggle", "default": False, "required": False},
    {"flag": "--max-retries", "name": "Max Retries", "type": "number", "default": 10, "required": False},
    {"flag": "--min-rate", "name": "Min Rate", "type": "number", "default": 0, "required": False},
    {"flag": "--max-rate", "name": "Max Rate", "type": "number", "default": 0, "required": False},
    {"flag": "--script-args", "name": "Script Args", "type": "text", "default": "", "required": False},
    {"flag": "--dns-servers", "name": "DNS Servers", "type": "text", "default": "", "required": False},
    {"flag": "-f", "name": "Fragment Packets", "type": "toggle", "default": False, "required": False},
    {"flag": "--mtu", "name": "MTU", "type": "number", "default": 0, "required": False}
]

# Nuclei
nuclei = [
    {"flag": "-severity", "name": "Severity", "type": "multiselect", "options": ["info", "low", "medium", "high", "critical"], "default": [], "required": False},
    {"flag": "-tags", "name": "Tags", "type": "text", "default": "", "required": False},
    {"flag": "-t", "name": "Templates", "type": "text", "default": "", "required": False},
    {"flag": "-rl", "name": "Rate Limit", "type": "number", "default": 150, "required": False},
    {"flag": "-c", "name": "Concurrency", "type": "number", "default": 25, "required": False},
    {"flag": "-retries", "name": "Retries", "type": "number", "default": 1, "required": False},
    {"flag": "-o", "name": "Output File", "type": "text", "default": "", "required": False},
    {"flag": "-jsonl", "name": "JSON Output", "type": "toggle", "default": False, "required": False},
    {"flag": "-me", "name": "Markdown Export", "type": "text", "default": "", "required": False},
    {"flag": "-l", "name": "Target List", "type": "file", "default": "", "required": False},
    {"flag": "-proxy", "name": "Proxy", "type": "text", "default": "", "required": False},
    {"flag": "-H", "name": "Headers", "type": "text", "default": "", "required": False}
]

# Subfinder
subfinder = [
    {"flag": "-s", "name": "Sources", "type": "multiselect", "options": ["alienvault", "anondns", "binaryedge", "bufferover", "censys", "certspotter", "chaos", "crtsh", "dnsdumpster"], "default": [], "required": False},
    {"flag": "-recursive", "name": "Recursive", "type": "toggle", "default": False, "required": False},
    {"flag": "-t", "name": "Threads", "type": "number", "default": 10, "required": False},
    {"flag": "-max-time", "name": "Timeout", "type": "number", "default": 10, "required": False},
    {"flag": "-rl", "name": "Rate Limit", "type": "number", "default": 0, "required": False},
    {"flag": "-silent", "name": "Silent", "type": "toggle", "default": False, "required": False},
    {"flag": "-json", "name": "JSON Output", "type": "toggle", "default": False, "required": False},
    {"flag": "-o", "name": "Output File", "type": "text", "default": "", "required": False},
    {"flag": "-r", "name": "Resolvers", "type": "file", "default": "", "required": False}
]

# Amass
amass = [
    {"flag": "-passive", "name": "Passive Mode", "type": "toggle", "default": False, "required": False},
    {"flag": "-active", "name": "Active Mode", "type": "toggle", "default": False, "required": False},
    {"flag": "-brute", "name": "Bruteforce", "type": "toggle", "default": False, "required": False},
    {"flag": "-rf", "name": "Resolvers", "type": "file", "default": "", "required": False},
    {"flag": "-w", "name": "Wordlists", "type": "file", "default": "", "required": False},
    {"flag": "-asn", "name": "ASN", "type": "text", "default": "", "required": False},
    {"flag": "-ip", "name": "IPs", "type": "toggle", "default": False, "required": False},
    {"flag": "-timeout", "name": "Timeout", "type": "number", "default": 10, "required": False},
    {"flag": "-o", "name": "Output File", "type": "text", "default": "", "required": False}
]

# Httpx
httpx = [
    {"flag": "-sc", "name": "Status Code", "type": "toggle", "default": False, "required": False},
    {"flag": "-title", "name": "Title", "type": "toggle", "default": False, "required": False},
    {"flag": "-td", "name": "Tech Detect", "type": "toggle", "default": False, "required": False},
    {"flag": "-tls", "name": "TLS Probes", "type": "toggle", "default": False, "required": False},
    {"flag": "-cdn", "name": "CDN Detection", "type": "toggle", "default": False, "required": False},
    {"flag": "-screenshot", "name": "Screenshot", "type": "toggle", "default": False, "required": False},
    {"flag": "-json", "name": "JSON Output", "type": "toggle", "default": False, "required": False},
    {"flag": "-p", "name": "Ports", "type": "text", "default": "", "required": False},
    {"flag": "-t", "name": "Threads", "type": "number", "default": 50, "required": False}
]

# Naabu
naabu = [
    {"flag": "-p", "name": "Ports", "type": "text", "default": "top-100", "required": False},
    {"flag": "-rate", "name": "Rate", "type": "number", "default": 1000, "required": False},
    {"flag": "-sn", "name": "Host Discovery", "type": "toggle", "default": False, "required": False},
    {"flag": "-exclude-ports", "name": "Exclude Ports", "type": "text", "default": "", "required": False},
    {"flag": "-json", "name": "JSON Output", "type": "toggle", "default": False, "required": False},
    {"flag": "-passive", "name": "Passive Port Enum", "type": "toggle", "default": False, "required": False}
]

# Katana
katana = [
    {"flag": "-d", "name": "Depth", "type": "number", "default": 3, "required": False},
    {"flag": "-hl", "name": "Headless", "type": "toggle", "default": False, "required": False},
    {"flag": "-jc", "name": "JavaScript Parsing", "type": "toggle", "default": False, "required": False},
    {"flag": "-e", "name": "Extensions", "type": "text", "default": "", "required": False},
    {"flag": "-proxy", "name": "Proxy", "type": "text", "default": "", "required": False},
    {"flag": "-rl", "name": "Rate Limit", "type": "number", "default": 150, "required": False},
    {"flag": "-c", "name": "Concurrency", "type": "number", "default": 10, "required": False}
]

# DNSX
dnsx = [
    {"flag": "-r", "name": "Resolvers", "type": "file", "default": "", "required": False},
    {"flag": "-a", "name": "A Record", "type": "toggle", "default": False, "required": False},
    {"flag": "-aaaa", "name": "AAAA Record", "type": "toggle", "default": False, "required": False},
    {"flag": "-cname", "name": "CNAME Record", "type": "toggle", "default": False, "required": False},
    {"flag": "-txt", "name": "TXT Record", "type": "toggle", "default": False, "required": False},
    {"flag": "-mx", "name": "MX Record", "type": "toggle", "default": False, "required": False},
    {"flag": "-ptr", "name": "PTR Record", "type": "toggle", "default": False, "required": False},
    {"flag": "-json", "name": "JSON Output", "type": "toggle", "default": False, "required": False}
]

# Shodan
shodan = [
    {"flag": "api_key", "name": "API Key", "type": "apikey", "default": "", "required": False},
    {"flag": "query", "name": "Query", "type": "text", "default": "", "required": False},
    {"flag": "filters", "name": "Filters", "type": "text", "default": "", "required": False},
    {"flag": "facets", "name": "Facets", "type": "text", "default": "", "required": False},
    {"flag": "export", "name": "Export", "type": "toggle", "default": False, "required": False}
]

def write_args(name, data):
    with open(os.path.join(OUT_DIR, f"{name}.json"), "w") as f:
        json.dump(data, f, indent=2)

write_args("nmap", nmap)
write_args("nuclei", nuclei)
write_args("subfinder", subfinder)
write_args("amass", amass)
write_args("httpx", httpx)
write_args("naabu", naabu)
write_args("katana", katana)
write_args("dnsx", dnsx)
write_args("shodan", shodan)
print("Generated arguments.")
