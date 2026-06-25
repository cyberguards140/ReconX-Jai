def get_presets(tool_id):
    presets = {
        "nmap": [
            {"name": "Quick Scan", "flags": {"-sV": True, "-Pn": True, "-T": "4"}},
            {"name": "Full Scan", "flags": {"-sV": True, "-sC": True, "-p": "1-65535", "-T": "4"}},
            {"name": "Stealth Scan", "flags": {"-sS": True, "-Pn": True, "-T": "2"}},
        ],
        "nuclei": [
            {"name": "Critical Only", "flags": {"-severity": ["critical", "high"], "-c": 50}},
            {"name": "Fast Scan", "flags": {"-c": 100, "-rl": 500}},
        ],
    }
    return presets.get(tool_id, [])
