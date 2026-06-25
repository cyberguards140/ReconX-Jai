from __future__ import annotations

import logging
import os
from typing import Any

try:
    from langchain_core.language_models.chat_models import BaseChatModel
    from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, SystemMessage
    from langchain_openai import ChatOpenAI

    HAS_LANGCHAIN = True
except ImportError:
    HAS_LANGCHAIN = False
    BaseChatModel = Any
    BaseMessage = Any
    HumanMessage = Any
    SystemMessage = Any
    AIMessage = Any

logger = logging.getLogger(__name__)


class LLMProvider:
    """
    Provider-agnostic LLM interface for the ReconX Copilot.
    Currently defaults to OpenAI (e.g., GPT-4o), but architected to support Azure,
    Anthropic, or local Ollama instances seamlessly.
    """

    def __init__(self, provider: str = "openai", model: str = "gpt-4o"):
        self.provider = provider
        self.model = model
        self.client: BaseChatModel | None = None

        self._initialize_client()

    def _initialize_client(self):
        if not HAS_LANGCHAIN:
            logger.warning("Langchain core is not installed. LLM features will be disabled.")
            return

        api_key = os.getenv("OPENAI_API_KEY")
        if self.provider == "openai" and api_key:
            self.client = ChatOpenAI(
                model=self.model,
                temperature=0.0,  # Zero temperature for analytical precision
                max_tokens=2048,
                api_key=api_key,
                streaming=True,
                max_retries=3,
            )
            logger.info(f"Initialized LLM Provider: {self.provider} ({self.model})")
        else:
            logger.warning(
                f"Failed to initialize LLM provider '{self.provider}'. Missing API key or unsupported."
            )

    async def ainvoke(
        self, messages: list[BaseMessage], tools: list[Any] | None = None
    ) -> BaseMessage:
        """
        Asynchronously invokes the LLM with a list of messages.
        Supports tool binding if the backend supports function calling.
        """
        if not self.client:
            raise ValueError(
                "LLM Client is not initialized. Ensure API keys and dependencies are present."
            )

        model = self.client
        if tools:
            # Bind tools (functions) to the model
            model = model.bind_tools(tools)

        try:
            response = await model.ainvoke(messages)
            return response
        except Exception as e:
            logger.error(f"LLM invocation failed: {e}")
            raise e


llm_provider = LLMProvider()
