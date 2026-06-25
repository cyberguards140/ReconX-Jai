class ReportEngine:
    """Generates structured report objects based on database stats."""

    @staticmethod
    def generate_executive_summary(asset_count: int, critical_count: int, high_count: int) -> dict:
        return {
            "title": "Executive Summary",
            "type": "executive",
            "overview": f"Assessed {asset_count} assets.",
            "risk_summary": {"critical": critical_count, "high": high_count},
        }

    @staticmethod
    def generate_technical_report(findings: list[dict]) -> dict:
        return {
            "title": "Technical Report",
            "type": "technical",
            "findings_count": len(findings),
            "findings": findings,
        }

    @staticmethod
    def generate_asset_inventory(assets: list[dict]) -> dict:
        return {"title": "Asset Inventory", "type": "inventory", "assets": assets}
