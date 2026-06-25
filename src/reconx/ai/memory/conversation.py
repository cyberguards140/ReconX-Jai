import logging
from collections import defaultdict

logger = logging.getLogger(__name__)


class ConversationMemory:
    """
    Manages conversational memory for the AI Security Copilot.
    Strictly segmented by tenant_id and session_id.
    """

    def __init__(self):
        # In memory mock. Replace with Redis or Postgres JSONB in production.
        # Structure: memory_store[tenant_id][session_id] = [Message, Message]
        self.memory_store = defaultdict(lambda: defaultdict(list))

    def add_message(self, tenant_id: str, session_id: str, role: str, content: str):
        """Adds a message to the session history."""
        self.memory_store[tenant_id][session_id].append({"role": role, "content": content})

    def get_history(self, tenant_id: str, session_id: str) -> list[dict[str, str]]:
        """Retrieves the message history for a specific session."""
        return self.memory_store[tenant_id].get(session_id, [])

    def clear_session(self, tenant_id: str, session_id: str):
        """Wipes the conversation memory for security/retention reasons."""
        if session_id in self.memory_store[tenant_id]:
            del self.memory_store[tenant_id][session_id]
            logger.info(f"Cleared memory for session {session_id} in tenant {tenant_id}")


conversation_memory = ConversationMemory()
