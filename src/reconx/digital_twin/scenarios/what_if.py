import copy
import logging
from typing import Any

from reconx.digital_twin.attack_models.simulator import attack_simulator
from reconx.digital_twin.defense_models.validator import defense_validator

logger = logging.getLogger(__name__)


class WhatIfScenarioEngine:
    """
    Provides a Decision Laboratory interface. Modifies a Twin Snapshot with theoretical changes
    and re-runs the attack simulator to measure risk reduction.
    """

    def __init__(self):
        pass

    def run_scenario(
        self, baseline_snapshot: dict[str, Any], theoretical_changes: list[dict[str, Any]]
    ) -> dict[str, Any]:
        """
        Injects theoretical changes into the snapshot and evaluates impact.
        """
        # Create a deep copy so we don't mutate the baseline
        test_snapshot = copy.deepcopy(baseline_snapshot)

        # Apply changes (e.g., {"action": "add_control", "type": "edr", "target": "a1"})
        for change in theoretical_changes:
            if change["action"] == "add_control":
                test_snapshot.get("controls", []).append(
                    {
                        "id": f"sim_c_{len(test_snapshot.get('controls', []))}",
                        "type": change["type"],
                        "coverage": change["targets"],
                    }
                )
                logger.info(f"Scenario Engine: Added theoretical {change['type']} control.")
            elif change["action"] == "patch_vulnerability":
                for asset in test_snapshot.get("assets", []):
                    if asset["id"] in change["targets"]:
                        if change["cve"] in asset.get("vulnerabilities", []):
                            asset["vulnerabilities"].remove(change["cve"])
                logger.info(f"Scenario Engine: Patched theoretical vulnerability {change['cve']}.")

        # Re-run simulation
        sim_results = attack_simulator.simulate_campaign(test_snapshot)
        val_results = defense_validator.validate_controls(test_snapshot, sim_results)

        return {
            "scenario_results": {
                "attack_success": sim_results["campaign_status"],
                "defense_coverage": val_results["coverage_score"],
                "gaps_remaining": len(val_results["gaps"]),
            }
        }


what_if_engine = WhatIfScenarioEngine()
