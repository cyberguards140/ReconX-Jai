from typing import Any


class AssetCorrelator:
    @staticmethod
    def correlate_findings(findings: list[dict[str, Any]]) -> list[dict[str, Any]]:
        # Merges findings with same asset, title, and severity across multiple sources
        correlated = {}
        for finding in findings:
            key = f"{finding.get('title')}:{finding.get('severity')}:{finding.get('asset_value')}"
            if key not in correlated:
                correlated[key] = finding.copy()
                correlated[key]["sources"] = [finding.get("source")]
            else:
                if finding.get("source") not in correlated[key]["sources"]:
                    correlated[key]["sources"].append(finding.get("source"))
        return list(correlated.values())
