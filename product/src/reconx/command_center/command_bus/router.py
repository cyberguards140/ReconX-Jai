import logging
from typing import Dict, Any

from reconx.autonomous.api.router import trigger_triage # Example cross-module dependency

logger = logging.getLogger(__name__)

class CommandBusRouter:
    """
    Unified Command Routing layer. Dispatches synchronous and asynchronous workflows
    (e.g., triggering Autonomous Remediation, launching an AI Copilot chat).
    """
    def __init__(self):
        # Dictionary of registered command handlers
        self.handlers = {
            "trigger_autonomous_triage": self._handle_triage
        }

    def _handle_triage(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Wrapper for triggering triage locally."""
        logger.info(f"CommandBus routing to Autonomous Triage: {payload.get('event_id')}")
        from reconx.autonomous.investigations.triage import triage_engine
        return triage_engine.triage_event(payload)

    def dispatch(self, command_name: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Executes a command through the central bus.
        """
        logger.info(f"CommandBus received command: {command_name}")
        
        handler = self.handlers.get(command_name)
        if not handler:
            logger.error(f"Unknown command: {command_name}")
            raise ValueError(f"Command '{command_name}' is not registered on the CommandBus.")
            
        try:
            result = handler(payload)
            return {
                "status": "success",
                "command": command_name,
                "result": result
            }
        except Exception as e:
            logger.error(f"CommandBus failed to execute {command_name}: {e}")
            return {
                "status": "error",
                "command": command_name,
                "message": str(e)
            }

command_bus = CommandBusRouter()
