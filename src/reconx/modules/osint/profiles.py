from enum import Enum


class OSINTProfile(str, Enum):
    QUICK = "quick"
    STANDARD = "standard"
    DEEP = "deep"


def get_osint_tools(profile: OSINTProfile) -> list[dict]:
    if profile == OSINTProfile.QUICK:
        return [{"id": "theharvester", "plugin": "theharvester", "depends_on": []}]
    elif profile == OSINTProfile.STANDARD:
        return [
            {"id": "theharvester", "plugin": "theharvester", "depends_on": []},
            {"id": "reconng", "plugin": "reconng", "depends_on": []},
        ]
    elif profile == OSINTProfile.DEEP:
        return [
            {"id": "theharvester", "plugin": "theharvester", "depends_on": []},
            {"id": "reconng", "plugin": "reconng", "depends_on": []},
            {"id": "holehe", "plugin": "holehe", "depends_on": ["theharvester", "reconng"]},
            {"id": "sherlock", "plugin": "sherlock", "depends_on": ["theharvester", "reconng"]},
        ]
    return []
