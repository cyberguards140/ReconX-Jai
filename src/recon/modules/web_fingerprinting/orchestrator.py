from typing import Any

from recon.modules.web_fingerprinting.profiles import WebProfile
from recon.modules.web_fingerprinting.workflows import WebWorkflowBuilder


class WebFingerprintingOrchestrator:
    @staticmethod
    async def run_web_recon(
        target: str, profile: WebProfile, user_id: str = "system"
    ) -> dict[str, Any]:
        """
        Builds a web fingerprinting workflow for the given profile and target.
        """
        workflow = WebWorkflowBuilder.build(target, profile)

        return {
            "status": "scheduled",
            "target": target,
            "profile": profile.value,
            "tasks": [t.plugin for t in workflow.tasks],
        }
