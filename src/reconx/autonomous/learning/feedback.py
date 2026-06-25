import logging

logger = logging.getLogger(__name__)


class FeedbackLoop:
    """
    Captures explicit analyst feedback (Approved/Rejected/Modified)
    to tune future recommendation confidence scores.
    """

    def __init__(self):
        # Memory mock. In production, writes to Neo4j or Postgres for analytics tracking
        self.feedback_store = []

    def capture_feedback(self, plan_id: str, action: str, analyst_id: str, feedback_text: str = ""):
        """
        Records the outcome of a recommended action.
        action can be 'approved', 'rejected', 'modified'.
        """
        record = {
            "plan_id": plan_id,
            "action": action,
            "analyst_id": analyst_id,
            "feedback": feedback_text,
        }
        self.feedback_store.append(record)

        if action == "rejected":
            logger.warning(
                f"ASO Recommendation {plan_id} was REJECTED by analyst {analyst_id}. Reason: {feedback_text}"
            )
        else:
            logger.info(f"ASO Feedback recorded for {plan_id}: {action}")

        # In an advanced setup, this would trigger a background task to recalculate
        # heuristic weights or fine-tune an ML model predicting recommendation success.


feedback_loop = FeedbackLoop()
