import logging
from enum import Enum

logger = logging.getLogger(__name__)


class WorkflowState(str, Enum):
    QUEUED = "Queued"
    RUNNING = "Running"
    COMPLETED = "Completed"
    FAILED = "Failed"
    CANCELLED = "Cancelled"


class TaskState(str, Enum):
    PENDING = "Pending"
    RUNNING = "Running"
    COMPLETED = "Completed"
    FAILED = "Failed"
    RETRYING = "Retrying"


class StateMachine:
    """
    Manages state transitions for SOAR workflows and tasks.
    """

    WORKFLOW_TRANSITIONS: dict[WorkflowState, list[WorkflowState]] = {
        WorkflowState.QUEUED: [
            WorkflowState.RUNNING,
            WorkflowState.CANCELLED,
            WorkflowState.FAILED,
        ],
        WorkflowState.RUNNING: [
            WorkflowState.COMPLETED,
            WorkflowState.FAILED,
            WorkflowState.CANCELLED,
        ],
        WorkflowState.COMPLETED: [],
        WorkflowState.FAILED: [],
        WorkflowState.CANCELLED: [],
    }

    TASK_TRANSITIONS: dict[TaskState, list[TaskState]] = {
        TaskState.PENDING: [TaskState.RUNNING, TaskState.FAILED],
        TaskState.RUNNING: [TaskState.COMPLETED, TaskState.FAILED, TaskState.RETRYING],
        TaskState.RETRYING: [TaskState.RUNNING, TaskState.FAILED],
        TaskState.COMPLETED: [],
        TaskState.FAILED: [],
    }

    @classmethod
    def can_transition_workflow(cls, current: WorkflowState, next_state: WorkflowState) -> bool:
        return next_state in cls.WORKFLOW_TRANSITIONS.get(current, [])

    @classmethod
    def can_transition_task(cls, current: TaskState, next_state: TaskState) -> bool:
        return next_state in cls.TASK_TRANSITIONS.get(current, [])

    @classmethod
    def validate_workflow_transition(cls, current: WorkflowState, next_state: WorkflowState):
        if not cls.can_transition_workflow(current, next_state):
            raise ValueError(f"Invalid workflow state transition: {current} -> {next_state}")

    @classmethod
    def validate_task_transition(cls, current: TaskState, next_state: TaskState):
        if not cls.can_transition_task(current, next_state):
            raise ValueError(f"Invalid task state transition: {current} -> {next_state}")
