from typing import Any

from recon.modules.smb.profiles import SMBProfile
from recon.modules.smb.workflows import SMBWorkflowBuilder


class SMBOrchestrator:
    @staticmethod
    async def run_smb_recon(
        target: str, profile: SMBProfile, user_id: str = "system"
    ) -> dict[str, Any]:
        workflow = SMBWorkflowBuilder.build(target, profile)

        return {
            "status": "scheduled",
            "target": target,
            "profile": profile.value,
            "tasks": [t.plugin for t in workflow.tasks],
        }
