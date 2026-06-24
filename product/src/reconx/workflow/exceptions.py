class WorkflowError(Exception):
    pass


class WorkflowValidationError(WorkflowError):
    pass


class WorkflowExecutionError(WorkflowError):
    pass


class DependencyCycleError(WorkflowError):
    pass


class TaskExecutionError(WorkflowError):
    pass
