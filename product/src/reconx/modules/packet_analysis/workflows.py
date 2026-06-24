from reconx.workflow.models.workflow import Workflow, WorkflowTask
from typing import List

def get_packet_tools(is_live: bool) -> List[dict]:
    if is_live:
        return [
            {"id": "tcpdump", "plugin": "tcpdump", "depends_on": []},
            {"id": "ngrep", "plugin": "ngrep", "depends_on": []}
        ]
    else:
        return [
            {"id": "tshark", "plugin": "tshark", "depends_on": []},
            {"id": "ngrep", "plugin": "ngrep", "depends_on": []}
        ]

class PacketWorkflowBuilder:
    @staticmethod
    def build(target: str, is_live: bool) -> Workflow:
        tasks_config = get_packet_tools(is_live)
        tasks = []
        for tc in tasks_config:
            tasks.append(WorkflowTask(
                id=tc["id"],
                plugin=tc["plugin"],
                depends_on=tc.get("depends_on", []),
                args=tc.get("args", {})
            ))
            
        mode = "live" if is_live else "offline"
        workflow_id = f"packet_{mode}_{target.replace('.', '_').replace('/', '_')}"
        return Workflow(id=workflow_id, name=f"Packet Analysis ({mode})", tasks=tasks)
