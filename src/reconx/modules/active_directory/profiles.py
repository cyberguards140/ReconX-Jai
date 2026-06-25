from enum import Enum
from typing import List

class ADProfile(str, Enum):
    QUICK = "quick"
    STANDARD = "standard"
    DEEP = "deep"

def get_ad_tools(profile: ADProfile) -> List[dict]:
    if profile == ADProfile.QUICK:
        return [
            {"id": "netexec", "plugin": "netexec", "depends_on": []}
        ]
    elif profile == ADProfile.STANDARD:
        return [
            {"id": "netexec", "plugin": "netexec", "depends_on": []},
            {"id": "ldapsearch", "plugin": "ldapsearch", "depends_on": []}
        ]
    elif profile == ADProfile.DEEP:
        return [
            {"id": "netexec", "plugin": "netexec", "depends_on": []},
            {"id": "ldapsearch", "plugin": "ldapsearch", "depends_on": []},
            {"id": "kerbrute", "plugin": "kerbrute", "depends_on": ["ldapsearch"]},
            {"id": "bloodhound", "plugin": "bloodhound", "depends_on": ["ldapsearch"]}
        ]
    return []
