from abc import ABC, abstractmethod

from core.models.asset import ReconAsset


class BaseParser(ABC):
    """
    Unified standard for all ReconX tool parsers.
    """

    @abstractmethod
    def parse(self, raw_line: str) -> ReconAsset | None:
        pass
