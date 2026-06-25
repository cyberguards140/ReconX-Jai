from typing import List, Dict, Set
from reconx.workflow.models.workflow import WorkflowTask as Task
from reconx.workflow.exceptions import DependencyCycleError

class DependencyGraph:
    def __init__(self, tasks: List[Task]):
        self.tasks = {t.id: t for t in tasks}
        self.graph: Dict[str, List[str]] = {t.id: [] for t in tasks}
        self.in_degree: Dict[str, int] = {t.id: 0 for t in tasks}
        self._build()

    def _build(self):
        for task in self.tasks.values():
            for dep in task.depends_on:
                self.graph[dep].append(task.id)
                self.in_degree[task.id] += 1

        self.validate_cycles()

    def validate_cycles(self):
        in_degree_copy = self.in_degree.copy()
        queue = [node for node, deg in in_degree_copy.items() if deg == 0]
        visited = 0

        while queue:
            node = queue.pop(0)
            visited += 1
            for neighbor in self.graph[node]:
                in_degree_copy[neighbor] -= 1
                if in_degree_copy[neighbor] == 0:
                    queue.append(neighbor)

        if visited != len(self.tasks):
            raise DependencyCycleError("Cycle detected in workflow tasks")

    def get_ready_tasks(self, completed_tasks: Set[str], failed_tasks: Set[str], current_running: Set[str]) -> List[Task]:
        """
        Returns tasks that are ready to run, ignoring any that have missing or failed dependencies.
        """
        ready = []
        for task_id, task in self.tasks.items():
            if task_id in completed_tasks or task_id in failed_tasks or task_id in current_running:
                continue

            deps_met = all(dep in completed_tasks for dep in task.depends_on)
            deps_failed = any(dep in failed_tasks for dep in task.depends_on)

            if deps_met and not deps_failed:
                ready.append(task)
        
        return ready

    def get_skipped_tasks(self, failed_tasks: Set[str], completed_tasks: Set[str]) -> Set[str]:
        """
        Returns tasks that should be skipped because their dependencies failed.
        """
        skipped = set()
        for task_id, task in self.tasks.items():
            if task_id in completed_tasks or task_id in failed_tasks:
                continue
            
            deps_failed = any((dep in failed_tasks or dep in skipped) for dep in task.depends_on)
            if deps_failed:
                skipped.add(task_id)
        return skipped
