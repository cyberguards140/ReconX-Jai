import logging
from typing import Dict, Any

from reconx.enterprise.isolation.tenant_context import get_current_tenant_id

logger = logging.getLogger(__name__)

class ApprovalWorkflowEngine:
    """
    Enforces Human-in-the-Loop (HITL) policies before Execution Plans run.
    """
    def __init__(self):
        # In memory pending queue. Prod -> Postgres.
        self.pending_approvals: Dict[str, Dict[str, Any]] = {}

    def evaluate_plan(self, plan: Dict[str, Any], risk_score: float) -> Dict[str, Any]:
        """
        Determines the level of approval required based on risk context.
        """
        tenant_id = get_current_tenant_id() or "system"
        plan_id = plan["plan_id"]
        
        # Policy Evaluation
        if risk_score < 30:
            approval_level = "auto_approved"
            status = "approved"
        elif risk_score < 70:
            approval_level = "manager_approval"
            status = "pending_approval"
        else:
            approval_level = "multi_level_approval"
            status = "pending_approval"
            
        plan["approval_level_required"] = approval_level
        plan["status"] = status
        
        if status == "pending_approval":
            self.pending_approvals[plan_id] = plan
            logger.info(f"Plan {plan_id} for tenant {tenant_id} queued for {approval_level}")
        else:
            logger.info(f"Plan {plan_id} auto-approved for tenant {tenant_id}")
            
        return plan

    def approve_plan(self, plan_id: str, user_id: str) -> bool:
        """
        A human operator explicitly approves a pending plan.
        """
        if plan_id in self.pending_approvals:
            self.pending_approvals[plan_id]["status"] = "approved"
            self.pending_approvals[plan_id]["approved_by"] = user_id
            
            # Forward to Orchestrator (Handled by API router logic)
            del self.pending_approvals[plan_id]
            logger.info(f"Plan {plan_id} explicitly approved by {user_id}")
            return True
        return False

approval_engine = ApprovalWorkflowEngine()
