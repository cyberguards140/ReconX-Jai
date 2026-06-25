from abc import ABC, abstractmethod
from typing import Any


class ReconXPlugin(ABC):
    """
    Phase 61: ReconX Plugin Base Class.
    External developers inherit from this to create 3rd-party intelligence tools.
    """

    @property
    @abstractmethod
    def plugin_name(self) -> str:
        pass

    @property
    @abstractmethod
    def plugin_version(self) -> str:
        pass

    @abstractmethod
    def execute(self, target: str, context: dict[str, Any]) -> list[dict[str, Any]]:
        """
        Executes the custom plugin logic against a target.
        Must return a list of findings or enrichments.
        """
        pass
