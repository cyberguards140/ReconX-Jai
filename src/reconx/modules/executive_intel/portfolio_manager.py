import uuid

from reconx.modules.executive_intel.schema import ProgramStatusModel


class PortfolioManager:
    """
    Tracks the health and completion status of long-term security remediation programs.
    """

    def __init__(self):
        self.programs = {}

    def init_program(self, name: str) -> ProgramStatusModel:
        prog = ProgramStatusModel(
            program_id=f"prog_{uuid.uuid4().hex[:8]}", name=name, status="Active", progress=0.0
        )
        self.programs[prog.program_id] = prog
        return prog

    def update_progress(self, program_id: str, new_progress: float):
        if program_id in self.programs:
            self.programs[program_id].progress = new_progress
            if new_progress >= 100.0:
                self.programs[program_id].status = "Completed"
