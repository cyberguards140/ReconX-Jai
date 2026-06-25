class AnalyticsCorrelationEngine:
    @staticmethod
    def merge_finding_duplicates(findings: list[dict]) -> list[dict]:
        merged = {}
        for finding in findings:
            key = f"{finding.get('asset_id')}-{finding.get('title')}"
            if key not in merged:
                merged[key] = finding
            else:
                merged[key]["sources"] = list(
                    set(merged[key].get("sources", []) + finding.get("sources", []))
                )
        return list(merged.values())
