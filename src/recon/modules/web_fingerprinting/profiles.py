from enum import Enum


class WebProfile(str, Enum):
    QUICK = "quick"
    STANDARD = "standard"
    DEEP = "deep"


def get_web_tools(profile: WebProfile) -> list[dict]:
    if profile == WebProfile.QUICK:
        return [
            {"id": "whatweb", "plugin": "whatweb", "args": {"mode": "standard"}, "depends_on": []}
        ]
    elif profile == WebProfile.STANDARD:
        return [
            {"id": "whatweb", "plugin": "whatweb", "args": {"mode": "standard"}, "depends_on": []},
            {"id": "wafw00f", "plugin": "wafw00f", "depends_on": []},
        ]
    elif profile == WebProfile.DEEP:
        return [
            {"id": "wafw00f", "plugin": "wafw00f", "depends_on": []},
            {
                "id": "whatweb",
                "plugin": "whatweb",
                "args": {"mode": "aggressive"},
                "depends_on": ["wafw00f"],
            },
        ]
    return []
