import json


def parse(json_line: str) -> dict:
    """
    Parses a Naabu JSON line to extract open ports.
    """
    try:
        data = json.loads(json_line)
    except json.JSONDecodeError:
        return None

    host = data.get("host")
    port = data.get("port")
    ip = data.get("ip")

    if not host or not port:
        return None

    return {"type": "port", "host": host, "ip": ip, "port": port, "relation": "has_port"}
