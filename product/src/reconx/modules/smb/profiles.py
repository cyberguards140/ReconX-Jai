from enum import Enum
from typing import List

class SMBProfile(str, Enum):
    QUICK = "quick"
    STANDARD = "standard"
    DEEP = "deep"

def get_smb_tools(profile: SMBProfile) -> List[dict]:
    if profile == SMBProfile.QUICK:
        return [
            {"id": "enum4linuxng", "plugin": "enum4linuxng", "depends_on": []}
        ]
    elif profile == SMBProfile.STANDARD:
        return [
            {"id": "enum4linuxng", "plugin": "enum4linuxng", "depends_on": []},
            {"id": "smbclient", "plugin": "smbclient", "depends_on": []}
        ]
    elif profile == SMBProfile.DEEP:
        return [
            {"id": "enum4linuxng", "plugin": "enum4linuxng", "depends_on": []},
            {"id": "smbclient", "plugin": "smbclient", "depends_on": []},
            {"id": "rpcclient", "plugin": "rpcclient", "depends_on": ["enum4linuxng"]}
        ]
    return []
