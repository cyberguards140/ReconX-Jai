import json

class NucleiParser:
    def extract(self, raw_output):
        assets = []
        try:
            for line in raw_output.splitlines():
                if line.startswith("{"):
                    data = json.loads(line)
                    assets.append({
                        "type": "finding",
                        "value": data.get("info", {}).get("name", "Unknown Finding"),
                        "severity": data.get("info", {}).get("severity", "info")
                    })
        except Exception:
            pass
        return assets
