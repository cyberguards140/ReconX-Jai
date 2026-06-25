def parse(line):
    line = line.strip()
    if not line:
        return None

    # Katana basic parsing: https://api.example.com/api/v1/users
    if line.startswith("http"):
        asset_type = "url"
        if "?" in line:
            asset_type = "parameter"
        elif "/api/" in line or "/v1/" in line or "/v2/" in line:
            asset_type = "endpoint"
        elif line.endswith(".js"):
            asset_type = "js_file"

        return {
            "type": "web_asset",
            "asset_type": asset_type,
            "value": line,
            "host": line.split("/")[2] if len(line.split("/")) > 2 else "unknown",
            "related": [],
        }
    return None
