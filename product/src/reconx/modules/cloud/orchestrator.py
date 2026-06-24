from typing import Dict, Any
from reconx.modules.cloud.enrichment import CloudEnricher
from reconx.modules.cloud.workflows import CloudWorkflowBuilder

class CloudOrchestrator:
    @staticmethod
    async def run_cloud_analysis(target: str, user_id: str = "system") -> Dict[str, Any]:
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
            "tasks": [t.plugin for t in workflow.tasks]
        }
