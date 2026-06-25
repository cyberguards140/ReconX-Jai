from .dependency_resolver import DependencyResolver
from .execution_graph import ExecutionGraph
from .scheduler import Scheduler


class Orchestrator:
    def __init__(self):
        self.resolver = DependencyResolver()
        self.scheduler = Scheduler()

    def run_pipeline(self, pipeline_stages):
        graph = ExecutionGraph()
        # Build graph logic
        execution_plan = self.resolver.resolve(graph)
        self.scheduler.execute(execution_plan)
