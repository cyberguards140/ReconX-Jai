from enum import Enum


class ContentProfile(str, Enum):
    QUICK = "quick"
    STANDARD = "standard"
    DEEP = "deep"


def get_content_tools(profile: ContentProfile) -> list[dict]:
    if profile == ContentProfile.QUICK:
        return [{"id": "gobuster", "plugin": "gobuster", "depends_on": []}]
    elif profile == ContentProfile.STANDARD:
        return [
            {"id": "gobuster", "plugin": "gobuster", "depends_on": []},
            {"id": "feroxbuster", "plugin": "feroxbuster", "depends_on": []},
        ]
    elif profile == ContentProfile.DEEP:
        return [
            {"id": "gobuster", "plugin": "gobuster", "depends_on": []},
            {"id": "feroxbuster", "plugin": "feroxbuster", "depends_on": []},
            {"id": "dirsearch", "plugin": "dirsearch", "depends_on": []},
            {"id": "ffuf", "plugin": "ffuf", "depends_on": ["gobuster", "feroxbuster"]},
            {"id": "wfuzz", "plugin": "wfuzz", "depends_on": ["ffuf"]},
        ]
    return []
