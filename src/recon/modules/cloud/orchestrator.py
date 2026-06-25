from typing import Any

from recon.modules.cloud.enrichment import CloudEnricher
from recon.modules.cloud.workflows import CloudWorkflowBuilder


class CloudOrchestrator:
    @staticmethod
    async def run_cloud_analysis(target: str, user_id: str = "system") -> dict[str, Any]:
        if CloudEnricher.is_aws_account(target):
            target_type = "aws"
        elif CloudEnricher.is_kubeconfig(target):
            target_type = "kubernetes"
        elif CloudEnricher.is_container_image(target):
            target_type = "container"
        else:
            target_type = "unknown"

        workflow = CloudWorkflowBuilder.build(target, target_type)

        return {
            "status": "scheduled",
            "target": target,
            "target_type": target_type,
            "tasks": [t.plugin for t in workflow.tasks],
        }
