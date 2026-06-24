class SubfinderParser:
    @staticmethod
    def parse(line):
        if "Found" in line and "subdomains" in line:
            return {"status": "Complete"}
        return None
