from core.legacy_core.argument_engine import ArgumentEngine
from core.legacy_core.validator import Validator
from core.legacy_core.parser_engine import ParserEngine
from core.legacy_core.normalization_engine import NormalizationEngine

class ToolAdapter:
    def __init__(self, tool_id, project_id, target):
        self.tool_id = tool_id
        self.project_id = project_id
        self.target = target
        self.config = {}

    def build_command(self):
        return ArgumentEngine.generate_command(self.tool_id, self.target, self.config)

    def validate(self):
        return Validator.validate_argument("target", self.target)

    def execute(self):
        if not self.validate():
            return None
        cmd = self.build_command()
        if not cmd:
            return None
        from core.legacy_core.execution_engine import ExecutionEngine
        job_id = ExecutionEngine.queue_job(self.tool_id, self.project_id, self.target, cmd)
        return job_id

    def parse_output(self, line):
        return ParserEngine.parse(self.tool_id, self.project_id, self.target, line)

    def normalize(self, parsed_data):
        NormalizationEngine.normalize_and_correlate(parsed_data, self.project_id, self.target, self.tool_id)
