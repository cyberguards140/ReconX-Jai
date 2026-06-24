class NucleiParser:
    @staticmethod
    def parse(line):
        # Example: [INF] Templates loaded: 1000
        if "Templates loaded:" in line:
            parts = line.split(":")
            if len(parts) > 1:
                return {"templates_loaded": parts[1].strip()}
        return None
