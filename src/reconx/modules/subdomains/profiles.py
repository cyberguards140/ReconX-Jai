from enum import Enum
from typing import List

class SubdomainProfile(str, Enum):
    QUICK = "quick"
    STANDARD = "standard"
    DEEP = "deep"

def get_subdomain_tools(profile: SubdomainProfile) -> List[dict]:
    if profile == SubdomainProfile.QUICK:
        return [
            {"id": "theharvester", "plugin": "theharvester", "depends_on": []}
        ]
    elif profile == SubdomainProfile.STANDARD:
        return [
            {"id": "theharvester", "plugin": "theharvester", "depends_on": []},
            {"id": "amass", "plugin": "amass", "args": {"mode": "passive"}, "depends_on": []},
            {"id": "dnsrecon", "plugin": "dnsrecon", "depends_on": ["amass"]}
        ]
    elif profile == SubdomainProfile.DEEP:
        return [
            {"id": "theharvester", "plugin": "theharvester", "depends_on": []},
            {"id": "amass", "plugin": "amass", "args": {"mode": "active"}, "depends_on": []},
            {"id": "dnsrecon", "plugin": "dnsrecon", "depends_on": ["amass"]},
            {"id": "dnsenum", "plugin": "dnsenum", "depends_on": ["amass"]},
            {"id": "fierce", "plugin": "fierce", "depends_on": ["amass"]}
        ]
    return []
