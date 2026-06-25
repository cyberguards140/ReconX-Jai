import pytest
from reconx.workflow.models.workflow import WorkflowTask as Task
from reconx.workflow.dependency_graph import DependencyGraph
from reconx.workflow.exceptions import DependencyCycleError

def test_linear_dag():
    tasks = [
        Task(id="A", plugin="test"),
        Task(id="B", plugin="test", depends_on=["A"]),
        Task(id="C", plugin="test", depends_on=["B"])
    ]
    graph = DependencyGraph(tasks)
    ready = graph.get_ready_tasks(set(), set(), set())
    assert len(ready) == 1
    assert ready[0].id == "A"

    ready = graph.get_ready_tasks({"A"}, set(), set())
    assert len(ready) == 1
    assert ready[0].id == "B"

def test_parallel_dag():
    tasks = [
        Task(id="A", plugin="test"),
        Task(id="B", plugin="test", depends_on=["A"]),
        Task(id="C", plugin="test", depends_on=["A"])
    ]
    graph = DependencyGraph(tasks)
    ready = graph.get_ready_tasks({"A"}, set(), set())
    assert len(ready) == 2
    ids = [t.id for t in ready]
    assert "B" in ids
    assert "C" in ids

def test_cycle_detection():
    tasks = [
        Task(id="A", plugin="test", depends_on=["C"]),
        Task(id="B", plugin="test", depends_on=["A"]),
        Task(id="C", plugin="test", depends_on=["B"])
    ]
    with pytest.raises(DependencyCycleError):
        DependencyGraph(tasks)

def test_skipped_tasks():
    tasks = [
        Task(id="A", plugin="test"),
        Task(id="B", plugin="test", depends_on=["A"]),
        Task(id="C", plugin="test", depends_on=["B"])
    ]
    graph = DependencyGraph(tasks)
    skipped = graph.get_skipped_tasks(failed_tasks={"A"}, completed_tasks=set())
    assert "B" in skipped
    assert "C" in skipped
