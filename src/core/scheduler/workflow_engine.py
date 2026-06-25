import logging
from typing import Any

logger = logging.getLogger(__name__)


class WorkflowEngine:
    """
    Evaluates JSON-based Directed Acyclic Graphs (DAGs) representing custom user workflows.
    Replaces static pipeline stages.
    """

    def __init__(self):
        # MVP In-memory storage of workflows
        self.workflows: dict[str, dict[str, Any]] = {}

    def register_workflow(self, workflow_id: str, workflow_json: dict[str, Any]):
        """Registers a new visual workflow."""
        self.workflows[workflow_id] = workflow_json
        logger.info(f"Registered workflow: {workflow_id}")

    def evaluate_next_stages(
        self, workflow_id: str, current_stage: str, context: dict[str, Any]
    ) -> list[str]:
        """
        Given the current state/stage and asset context, evaluate the DAG conditions
        to determine the next queue(s) to push the asset into.
        """
        workflow = self.workflows.get(workflow_id)
        if not workflow:
            logger.error(f"Workflow {workflow_id} not found.")
            return []

        # Find transitions originating from current_stage
        transitions = workflow.get("transitions", [])
        next_stages = []

        for transition in transitions:
            if transition.get("from") == current_stage:
                condition = transition.get("condition")
                if self._evaluate_condition(condition, context):
                    next_stages.append(transition.get("to"))

        return next_stages

    def _evaluate_condition(self, condition: dict[str, Any], context: dict[str, Any]) -> bool:
        """
        Evaluates a simple JSON rule against the context.
        e.g. {"field": "type", "operator": "==", "value": "subdomain"}
        """
        if not condition:
            return True  # Unconditional transition

        field = condition.get("field")
        op = condition.get("operator")
        val = condition.get("value")

        ctx_val = context.get(field)

        if op == "==":
            return ctx_val == val
        elif op == "!=":
            return ctx_val != val
        elif op == "in":
            return ctx_val in val

        return False


workflow_engine = WorkflowEngine()
