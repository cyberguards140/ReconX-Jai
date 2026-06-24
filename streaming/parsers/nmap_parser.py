class NmapParser:
    @staticmethod
    def parse(line):
        if "Initiating Ping Scan" in line:
            return {"phase": "Host Discovery"}
        elif "Initiating SYN Stealth Scan" in line:
            return {"phase": "Port Scan"}
        elif "Initiating Service scan" in line:
            return {"phase": "Service Scan"}
        elif "Initiating OS detection" in line:
            return {"phase": "OS Detection"}
        return None
