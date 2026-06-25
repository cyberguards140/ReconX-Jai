import uuid

from recon.modules.executive_intel.schema import RiskModel


class RiskGovernanceEngine:
    """
    Calculates Enterprise Risk Score based on Technical Risk, Criticality, Exposure, and Compliance.
    """

    def __init__(self):
        self.risk_register = {}

    def calculate_enterprise_risk(
        self, technical_score: int, criticality: str, compliance_impact: bool
    ) -> int:
        score = technical_score
        if criticality == "High":
            score += 30
        elif criticality == "Medium":
            score += 15

        if compliance_impact:
            score += 20

        return min(100, score)

    def log_risk(self, title: str, score: int) -> RiskModel:
        severity = "Critical" if score > 80 else ("High" if score > 60 else "Medium")
        risk = RiskModel(
            risk_id=f"rsk_{uuid.uuid4().hex[:8]}",
            title=title,
            business_impact="High" if score > 70 else "Medium",
            likelihood="High",
            severity=severity,
        )
        self.risk_register[risk.risk_id] = risk
        return risk
