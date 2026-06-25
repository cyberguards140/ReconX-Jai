class SubfinderParser:
    def extract(self, raw_output):
        assets = []
        for line in raw_output.splitlines():
            line = line.strip()
            if line and not line.startswith("["):
                assets.append({"type": "subdomain", "value": line})
        return assets
