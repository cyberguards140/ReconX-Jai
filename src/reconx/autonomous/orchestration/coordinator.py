import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class ExecutionCoordinator:
    """
    Supervises agent execution once an action is explicitly approved by a human.
    Routes tasks securely to workflow execution runners (e.g., Celery).
    """
    def __init__(self):
        pass

    def execute_plan(self, plan: Dict[str, Any]):
        """
        Takes an approved Execution Plan and dispatches it to the workflow engine.
        """
        if plan.get("status") != "approved":
            logger.error(f"Cannot execute plan {plan.get('plan_id')}. Status is {plan.get('status')}")
            raise ValueError("Plan must be in 'approved' status before execution.")
            
        logger.info(f"Orchestrating execution for plan {plan.get('plan_id')}")
        
        for step in plan.get("steps", []):
            logger.debug(f"Dispatching Action: {step.get('action')} on Target: {step.get('target')}")
            # Mock: In production, send task to Celery Message Broker
            # celery_app.send_task(step["action"], args=[step["target"]])
            step["status"] = "dispatched"
            
        plan["status"] = "in_progress"
        return plan

coordinator = ExecutionCoordinator()
