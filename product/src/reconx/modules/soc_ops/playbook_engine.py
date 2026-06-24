import uuid
from reconx.modules.soc_ops.schema import PlaybookModel
from typing import List

class PlaybookEngine:
    """
    Defines and associates structured response procedures.
    """
    def __init__(self):
        self.playbooks = {}

    def register_playbook(self, name: str, severity: str, steps: List[str]) -> PlaybookModel:
        pb = PlaybookModel(
            playbook_id=f"pb_{uuid.uuid4().hex[:8]}",
            name=name,
            severity=severity,
            steps=steps
        )
        self.playbooks[pb.playbook_id] = pb
        return pb

    def get_recommended_playbooks(self, severity: str) -> List[PlaybookModel]:
        return [pb for pb in self.playbooks.values() if pb.severity == severity]
