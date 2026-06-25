from typing import Any

from recon.modules.osint.profiles import OSINTProfile
from recon.modules.osint.workflows import OSINTWorkflowBuilder


class OSINTOrchestrator:
    @staticmethod
    async def run_osint_recon(
        target: str, profile: OSINTProfile, user_id: str = "system"
    ) -> dict[str, Any]:
        workflow = OSINTWorkflowBuilder.build(target, profile)

        return {
            "status": "scheduled",
            "target": target,
            "profile": profile.value,
            "tasks": [t.plugin for t in workflow.tasks],
        }
