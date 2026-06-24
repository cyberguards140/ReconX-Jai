class CVEEngine:
    @staticmethod
    def get_cve_details(cve_id: str) -> dict:
        return {"cve_id": cve_id, "cvss": 9.8, "severity": "CRITICAL"}
