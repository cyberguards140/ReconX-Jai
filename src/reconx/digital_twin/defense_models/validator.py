import logging
from typing import Any

logger = logging.getLogger(__name__)


class DefensiveValidator:
    """
    Evaluates theoretically deployed security controls against simulated attack chains.
    Produces Coverage Scores and Gap Reports.
    """

    def __init__(self):
        pass

    def validate_controls(
        self, twin_snapshot: dict[str, Any], attack_results: dict[str, Any]
    ) -> dict[str, Any]:
        """
        Determines if the current controls would have detected or blocked the attack.
        """
        controls = twin_snapshot.get("controls", [])
        attack_chain = attack_results.get("attack_chain", [])

        detected_steps = []
        blocked_steps = []

        for step in attack_chain:
            target = step["target"]
            tactic = step["tactic"]

            # Very basic heuristic: if target has a control, it might detect it.
            for control in controls:
                if target in control.get("coverage", []):
                    if control["type"] == "firewall" and tactic == "Initial Access":
                        blocked_steps.append(step)
                    elif control["type"] == "edr":
                        detected_steps.append(step)

        total_steps = len(attack_chain)
        coverage_score = (len(detected_steps) / total_steps * 100) if total_steps > 0 else 100.0

        return {
            "coverage_score": coverage_score,
            "detected_steps": detected_steps,
            "blocked_steps": blocked_steps,
            "gaps": [s for s in attack_chain if s not in detected_steps and s not in blocked_steps],
        }


defense_validator = DefensiveValidator()
