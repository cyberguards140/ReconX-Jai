from typing import Dict, Any
from reconx.modules.web_assessment.profiles import AssessmentProfile
from reconx.modules.web_assessment.workflows import AssessmentWorkflowBuilder

class WebAssessmentOrchestrator:
    @staticmethod
    async def run_assessment(target: str, profile: AssessmentProfile, user_id: str = "system") -> Dict[str, Any]:
        workflow = AssessmentWorkflowBuilder.build(target, profile)
        
        return {
            "status": "scheduled",
            "target": target,
            "profile": profile.value,
            "tasks": [t.plugin for t in workflow.tasks]
        }
