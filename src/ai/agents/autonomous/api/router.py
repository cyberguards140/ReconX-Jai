from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from ai.agents.autonomous.approvals.workflow import approval_engine
from ai.agents.autonomous.governance.auditor import decision_auditor
from ai.agents.autonomous.investigations.triage import triage_engine
from ai.agents.autonomous.orchestration.coordinator import coordinator
from ai.agents.autonomous.recommendations.generator import recommendation_engine
from ai.agents.autonomous.remediation.planner import remediation_planner
from core.auth.middleware import SecurityMiddleware
from plugins.enterprise.isolation.tenant_context import get_current_tenant_id

router = APIRouter(tags=["Autonomous Operations"], dependencies=[Depends(SecurityMiddleware)])


class EventRequest(BaseModel):
    event: dict[str, Any]


class ApprovalRequest(BaseModel):
    plan_id: str


@router.post("/triage", summary="Trigger Autonomous Triage")
async def trigger_triage(request: EventRequest):
    """
    Ingests a raw security event, triages it, builds a recommendation,
    constructs an execution plan, and routes it to the approval engine.
    """
    tenant_id = get_current_tenant_id()
    if not tenant_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Tenant context missing"
        )

    # 1. Triage
    triage_case = triage_engine.triage_event(request.event)

    # 2. Recommend
    recommendation = recommendation_engine.generate(triage_case)

    # 3. Plan Remediation
    plan = remediation_planner.create_execution_plan(recommendation)

    # 4. Request Approval
    risk_score = triage_case.get("scoring", {}).get("risk_score", 0.0)
    final_plan = approval_engine.evaluate_plan(plan, risk_score)

    # 5. Audit Logging
    decision_auditor.log_decision(
        plan["plan_id"], "generated_plan", {"risk": risk_score, "status": final_plan["status"]}
    )

    return {"message": "Triage complete", "plan": final_plan}


@router.post("/approve", summary="Approve an Autonomous Execution Plan")
async def approve_plan(request: ApprovalRequest):
    """
    Allows a human operator to explicitly approve a pending execution plan.
    """
    # Mocking user ID. In production, extract from JWT claims.
    user_id = "analyst_123"

    success = approval_engine.approve_plan(request.plan_id, user_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Plan not found or not pending approval."
        )

    # Execute the approved plan
    plan_to_execute = {
        "plan_id": request.plan_id,
        "status": "approved",
        "steps": [],
    }  # Mocked retrieval
    executed_plan = coordinator.execute_plan(plan_to_execute)

    # Audit
    decision_auditor.log_decision(
        request.plan_id, "approved_and_executed", {"approved_by": user_id}
    )

    return {"message": "Plan approved and execution orchestrated", "plan": executed_plan}


# Note: GET /decisions, POST /hunt, etc., would follow similar structural patterns.
