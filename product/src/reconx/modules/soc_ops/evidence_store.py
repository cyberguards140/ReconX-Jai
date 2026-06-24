import uuid
from datetime import datetime, timezone
from reconx.modules.soc_ops.schema import EvidenceModel
from typing import List

class EvidenceStore:
    """
    Manages the indexing and storage references for digital evidence.
    """
    def __init__(self):
        self.evidence_vault = []

    def log_evidence(self, ev_type: str, source: str, refs: List[str]) -> EvidenceModel:
        evidence = EvidenceModel(
            evidence_id=f"ev_{uuid.uuid4().hex[:8]}",
            evidence_type=ev_type,
            source=source,
            timestamp=datetime.now(timezone.utc).isoformat(),
            references=refs
        )
        self.evidence_vault.append(evidence)
        return evidence
