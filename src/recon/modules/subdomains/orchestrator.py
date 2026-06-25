from typing import Any

from recon.modules.subdomains.profiles import SubdomainProfile
from recon.modules.subdomains.workflows import SubdomainWorkflowBuilder


class SubdomainOrchestrator:
    @staticmethod
    async def run_subdomain_recon(
        domain: str, profile: SubdomainProfile, user_id: str = "system"
    ) -> dict[str, Any]:
        """
        Builds a subdomain enumeration workflow.
        """
        workflow = SubdomainWorkflowBuilder.build(domain, profile)

        return {
            "status": "scheduled",
            "target": domain,
            "profile": profile.value,
            "tasks": [t.plugin for t in workflow.tasks],
        }
