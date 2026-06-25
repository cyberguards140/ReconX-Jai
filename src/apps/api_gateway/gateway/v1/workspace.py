import uuid
from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from apps.api_gateway.gateway.router_registry import registry

router = APIRouter()
registry.register(router, prefix="/workspace", version="v1", tags=["workspace"])

# Mock DB for MVP
MOCK_CASES = {}


class InvestigationCase(BaseModel):
    title: str
    description: str


@router.post("/cases")
async def create_case(case: InvestigationCase) -> dict[str, Any]:
    """
    Creates a new Analyst Investigation Case.
    """
    case_id = str(uuid.uuid4())
    MOCK_CASES[case_id] = {
        "id": case_id,
        "title": case.title,
        "description": case.description,
        "status": "open",
        "evidence": [],
    }
    return MOCK_CASES[case_id]


@router.post("/cases/{case_id}/evidence")
async def add_evidence(case_id: str, evidence: dict[str, Any]) -> dict[str, Any]:
    """
    Attaches evidence (asset IDs, screenshots, notes) to a case.
    """
    if case_id not in MOCK_CASES:
        raise HTTPException(status_code=404, detail="Case not found")

    evidence_id = str(uuid.uuid4())
    evidence_payload = {
        "id": evidence_id,
        "type": evidence.get("type", "note"),
        "data": evidence.get("data", ""),
    }

    MOCK_CASES[case_id]["evidence"].append(evidence_payload)
    return MOCK_CASES[case_id]


@router.get("/cases/{case_id}")
async def get_case(case_id: str) -> dict[str, Any]:
    if case_id not in MOCK_CASES:
        raise HTTPException(status_code=404, detail="Case not found")
    return MOCK_CASES[case_id]
