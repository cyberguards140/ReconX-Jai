import uuid
from datetime import datetime, timezone

from reconx.modules.soc_ops.schema import CaseModel


class CaseManager:
    """
    Manages the state machine and lifecycle of an investigation.
    """

    def __init__(self):
        self.cases = {}

    def create_case(
        self, title: str, severity: str, alerts: list[str], assets: list[str]
    ) -> CaseModel:
        case = CaseModel(
            case_id=f"case_{uuid.uuid4().hex[:8]}",
            title=title,
            severity=severity,
            created_at=datetime.now(timezone.utc).isoformat(),
            linked_alerts=alerts,
            linked_assets=assets,
        )
        self.cases[case.case_id] = case
        return case

    def update_status(self, case_id: str, new_status: str):
        if case_id in self.cases:
            self.cases[case_id].status = new_status
