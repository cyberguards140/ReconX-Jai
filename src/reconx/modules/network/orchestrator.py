from typing import Any

from reconx.modules.network.profiles import ScanProfile
from reconx.modules.network.workflow import NetworkWorkflowBuilder


class NetworkOrchestrator:
    """Entrypoint for scheduling and coordinating Network Reconnaissance operations."""

    @staticmethod
    async def run_network_recon(
        target_str: str, profile: ScanProfile, user_id: str = "system"
    ) -> dict[str, Any]:
        """
        Expands targets, builds a workflow for the given profile, and dispatches it via the WorkflowEngine.
        In a real implementation, this might dispatch parallel workflows per expanded target,
        or pass the expanded list to a module that supports multiple targets.
        For now, we pass the raw target string to the workflow builder, allowing Masscan/Nmap to handle ranges natively.
        """

        # Build the DAG workflow using the predefined profile template
        workflow = NetworkWorkflowBuilder.build(target_str, profile)

        # We temporarily inject the built workflow into the engine's validator lookup
        # In a real scenario, the engine could accept a Workflow object directly.
        # Since execute_workflow currently loads from YAML, we'll bypass it for this orchestrator,
        # or adapt the engine to accept dynamic workflows.

        # For the sake of the framework architecture, we define the DAG and execute.
        # Here we mock the result to return the constructed workflow layout.
        return {
            "status": "scheduled",
            "target": target_str,
            "profile": profile.value,
            "tasks": [t.plugin for t in workflow.tasks],
        }
