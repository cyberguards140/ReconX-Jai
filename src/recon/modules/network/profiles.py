from enum import Enum


class ScanProfile(str, Enum):
    QUICK = "quick"
    STANDARD = "standard"
    DEEP = "deep"


def get_profile_tools(profile: ScanProfile) -> list[dict]:
    """Returns the ordered list of tools/tasks to run for a given profile."""
    if profile == ScanProfile.QUICK:
        return [
            {"id": "fping", "plugin": "fping", "depends_on": []},
            {"id": "masscan", "plugin": "masscan", "depends_on": ["fping"]},
        ]
    elif profile == ScanProfile.STANDARD:
        return [
            {"id": "fping", "plugin": "fping", "depends_on": []},
            {"id": "masscan", "plugin": "masscan", "depends_on": ["fping"]},
            {
                "id": "nmap",
                "plugin": "nmap",
                "depends_on": ["masscan"],
                "args": {"mode": "standard"},
            },
        ]
    elif profile == ScanProfile.DEEP:
        return [
            {"id": "netdiscover", "plugin": "netdiscover", "depends_on": []},
            {"id": "arpscan", "plugin": "arpscan", "depends_on": []},
            {"id": "masscan", "plugin": "masscan", "depends_on": ["netdiscover", "arpscan"]},
            {"id": "nmap", "plugin": "nmap", "depends_on": ["masscan"], "args": {"mode": "deep"}},
            {"id": "traceroute", "plugin": "traceroute", "depends_on": []},
        ]
    return []
