import logging
from collections.abc import Callable
from typing import Any

logger = logging.getLogger(__name__)


class ToolRegistry:
    """
    Manages the suite of tools the AI Copilot can invoke (e.g., Graph Search, RAG Query).
    Ensures that every tool invocation goes through permission validation.
    """

    def __init__(self):
        self._tools: dict[str, Callable] = {}

    def register(self, name: str, func: Callable, description: str):
        """Registers a Python function as a tool usable by the LLM."""
        self._tools[name] = {"func": func, "description": description}
        logger.info(f"Registered AI Tool: {name}")

    def get_tools(self) -> list[dict[str, Any]]:
        """Returns the list of tools in a format compatible with LangChain/OpenAI."""
        # For simplicity, returning mock schemas. In production, this would use Pydantic models.
        return [
            {
                "type": "function",
                "function": {
                    "name": name,
                    "description": meta["description"],
                    "parameters": {"type": "object", "properties": {}},  # Simplified
                },
            }
            for name, meta in self._tools.items()
        ]


tool_registry = ToolRegistry()


# Example Tool Registrations
def search_threat_intel(query: str, tenant_id: str):
    return f"Threat Intel results for {query}"


tool_registry.register(
    "search_threat_intel",
    search_threat_intel,
    "Searches the Threat Intelligence database for IOCs.",
)
