import uuid

from recon.modules.executive_intel.schema import ComplianceRequirementModel


class ComplianceEngine:
    """
    Maps low-level security events and misconfigurations to high-level framework requirements.
    """

    def __init__(self):
        self.mappings = []

    def evaluate_control(
        self, framework: str, control: str, passed: bool
    ) -> ComplianceRequirementModel:
        status = "Passed" if passed else "Failed"
        req = ComplianceRequirementModel(
            requirement_id=f"req_{uuid.uuid4().hex[:8]}",
            framework=framework,
            control=control,
            status=status,
        )
        self.mappings.append(req)
        return req
