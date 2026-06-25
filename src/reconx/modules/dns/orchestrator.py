from typing import Dict, Any
from reconx.modules.dns.profiles import DNSProfile
from reconx.modules.dns.workflows import DNSWorkflowBuilder

class DNSOrchestrator:
    @staticmethod
    async def run_dns_recon(domain: str, profile: DNSProfile, user_id: str = "system") -> Dict[str, Any]:
        """
        Builds a DNS intelligence workflow for the given profile and domain.
        """
        workflow = DNSWorkflowBuilder.build(domain, profile)
        
        return {
            "status": "scheduled",
            "target": domain,
            "profile": profile.value,
            "tasks": [t.plugin for t in workflow.tasks]
        }
