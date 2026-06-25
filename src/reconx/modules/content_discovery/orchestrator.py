from typing import Dict, Any
from reconx.modules.content_discovery.profiles import ContentProfile
from reconx.modules.content_discovery.workflows import ContentWorkflowBuilder

class ContentDiscoveryOrchestrator:
    @staticmethod
    async def run_content_recon(target: str, profile: ContentProfile, user_id: str = "system") -> Dict[str, Any]:
        """
        Builds a content discovery workflow for the given profile and target.
        """
        workflow = ContentWorkflowBuilder.build(target, profile)
        
        return {
            "status": "scheduled",
            "target": target,
            "profile": profile.value,
            "tasks": [t.plugin for t in workflow.tasks]
        }
