from typing import Any


class VisualCache:
    """
    Abstract caching layer to prevent re-rendering visual topologies constantly.
    """

    def __init__(self):
        self._cache = {}

    def get_layout(self, graph_id: str) -> dict[str, Any] | None:
        return self._cache.get(f"layout_{graph_id}")

    def set_layout(self, graph_id: str, layout_data: dict[str, Any]):
        self._cache[f"layout_{graph_id}"] = layout_data
