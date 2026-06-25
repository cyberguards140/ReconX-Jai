from enum import Enum
from typing import List

class DNSProfile(str, Enum):
    QUICK = "quick"
    STANDARD = "standard"
    DEEP = "deep"

def get_dns_profile_tools(profile: DNSProfile) -> List[dict]:
    if profile == DNSProfile.QUICK:
        return [
            {"id": "dig", "plugin": "dig", "depends_on": []},
            {"id": "host", "plugin": "host", "depends_on": []},
            {"id": "whois", "plugin": "whois", "depends_on": []}
        ]
    elif profile == DNSProfile.STANDARD:
        return [
            {"id": "whois", "plugin": "whois", "depends_on": []},
            {"id": "dnsrecon", "plugin": "dnsrecon", "depends_on": ["whois"]},
            {"id": "dnsenum", "plugin": "dnsenum", "depends_on": ["whois"]}
        ]
    elif profile == DNSProfile.DEEP:
        return [
            {"id": "whois", "plugin": "whois", "depends_on": []},
            {"id": "dnsrecon", "plugin": "dnsrecon", "depends_on": ["whois"]},
            {"id": "dnsenum", "plugin": "dnsenum", "depends_on": ["whois"]},
            {"id": "fierce", "plugin": "fierce", "depends_on": ["dnsrecon", "dnsenum"]},
            {"id": "dig", "plugin": "dig", "depends_on": ["fierce"]},
            {"id": "host", "plugin": "host", "depends_on": ["fierce"]},
            {"id": "nslookup", "plugin": "nslookup", "depends_on": ["fierce"]}
        ]
    return []
