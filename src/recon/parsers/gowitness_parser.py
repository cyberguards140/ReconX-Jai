import json


def parse(json_line: str) -> dict:
    """
    Parses a Gowitness JSON line and extracts visual intelligence and login heuristics.
    """
    try:
        data = json.loads(json_line)
    except json.JSONDecodeError:
        return None

    url = data.get("url")
    if not url:
        return None

    screenshot_uri = data.get("screenshot_path", "")
    page_title = data.get("title", "")
    page_hash = data.get("hash", "")

    # Login page heuristics
    is_login_portal = False
    login_patterns = ["login", "signin", "sso", "auth", "portal", "dashboard"]

    # Check title
    if any(pattern in page_title.lower() for pattern in login_patterns):
        is_login_portal = True

    return {
        "type": "screenshot",
        "url": url,
        "screenshot_uri": screenshot_uri,
        "page_title": page_title,
        "page_hash": page_hash,
        "is_login_portal": is_login_portal,
        "relation": "has_screenshot",
    }
