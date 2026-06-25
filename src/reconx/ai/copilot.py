import logging
from typing import Any

try:
    from langchain_core.messages import AIMessage, HumanMessage, SystemMessage, ToolMessage
except ImportError:
    pass

from reconx.ai.agents.orchestrator import orchestrator_agent
from reconx.ai.explainability.tracker import explainability_tracker
from reconx.ai.governance.safety import safety_guard

logger = logging.getLogger(__name__)


class SecurityCopilot:
    """
    The core AI engine. Glues together the LLM provider, Safety Boundaries, and the Multi-Agent Orchestrator.
    """

    def __init__(self):
        self.system_prompt = SystemMessage(
            content=(
                "You are the ReconX AI Security Copilot, a senior enterprise security intelligence analyst. "
                "You have access to a powerful platform spanning Threat Intelligence, Graph Relationships, "
                "and Attack Surface Management. "
                "Always adhere strictly to tenant boundaries. Base all assertions on data retrieved via your tools. "
                "Provide highly analytical, zero-trust aligned reasoning."
            )
        )

    async def chat(self, user_input: str, tenant_id: str, session_id: str) -> dict[str, Any]:
        """
        Processes a natural language query through the Copilot pipeline.
        """
        # 1. Safety & Governance (Prompt Injection Check)
        if not safety_guard.is_safe(user_input):
            return {
                "response": "Your request violated security policies or triggered prompt injection protections.",
                "confidence": 0.0,
                "sources": [],
            }

        # 2. Delegate to the Orchestrator
        # The Orchestrator decides if we need to call RAG, Graph API, or Threat tools
        logger.info(f"Copilot routing request for tenant {tenant_id}: {user_input[:50]}...")

        try:
            # We pass the raw input to the orchestrator to resolve the objective
            orchestration_result = await orchestrator_agent.execute(user_input, tenant_id)

            # 3. Explainability & Packaging
            final_response = explainability_tracker.package_response(
                response_text=orchestration_result["output"],
                sources=orchestration_result.get("sources", []),
                reasoning_chain=orchestration_result.get("reasoning_chain", []),
            )

            return final_response

        except Exception as e:
            logger.error(f"Copilot encountered a failure: {e}", exc_info=True)
            return {
                "response": "An internal error occurred while processing the intelligence request.",
                "confidence": 0.0,
                "sources": [],
            }


copilot_engine = SecurityCopilot()
