from recon.modules.web_assessment.profiles import AssessmentProfile, get_assessment_tools
from platform_core.workflow_engine.workflow.models.workflow import Workflow, WorkflowTask


class AssessmentWorkflowBuilder:
    @staticmethod
    def build(target: str, profile: AssessmentProfile) -> Workflow:
        tasks_config = get_assessment_tools(profile)
        tasks = []
        for tc in tasks_config:
            tasks.append(
                WorkflowTask(
                    id=tc["id"],
                    plugin=tc["plugin"],
                    depends_on=tc.get("depends_on", []),
                    args=tc.get("args", {}),
                )
            )

        workflow_id = f"assess_{profile.value}_{target.replace('://', '_').replace('.', '_').replace('/', '')}"
        return Workflow(id=workflow_id, name=f"Web Assessment ({profile.value})", tasks=tasks)
