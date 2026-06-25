from typing import Any

from recon.modules.active_directory.profiles import ADProfile
from recon.modules.active_directory.workflows import ADWorkflowBuilder


class ADOrchestrator:
    @staticmethod
    async def run_ad_recon(
        target: str, profile: ADProfile, user_id: str = "system"
    ) -> dict[str, Any]:
        workflow = ADWorkflowBuilder.build(target, profile)

        return {
            "status": "scheduled",
            "target": target,
            "profile": profile.value,
            "tasks": [t.plugin for t in workflow.tasks],
        }
