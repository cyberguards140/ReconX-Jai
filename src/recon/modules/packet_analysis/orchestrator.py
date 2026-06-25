from typing import Any

from recon.modules.packet_analysis.capture import CaptureSource
from recon.modules.packet_analysis.workflows import PacketWorkflowBuilder


class PacketOrchestrator:
    @staticmethod
    async def run_packet_analysis(target: str, user_id: str = "system") -> dict[str, Any]:
        is_live = CaptureSource.is_interface(target)
        workflow = PacketWorkflowBuilder.build(target, is_live)

        return {
            "status": "scheduled",
            "target": target,
            "mode": "live" if is_live else "offline",
            "tasks": [t.plugin for t in workflow.tasks],
        }
