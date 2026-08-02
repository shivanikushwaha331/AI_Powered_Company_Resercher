"""
LLM Client Wrapper Module.
Provides an async interface for invoking Google Gemini or OpenAI LLMs.
"""

from typing import AsyncGenerator, Optional
from app.core.config import settings
from app.core.logging import logger


class LLMClient:
    """Async client wrapper for Google Gemini and OpenAI model inference."""

    def __init__(self, model_name: Optional[str] = None):
        self.model_name = model_name or settings.DEFAULT_LLM_MODEL

    async def generate_text(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """Generates text completion asynchronously."""
        logger.info(f"Generating LLM response using model {self.model_name}")
        # Placeholder skeleton
        raise NotImplementedError("LLM text generation client to be implemented.")

    async def generate_stream(
        self, prompt: str, system_prompt: Optional[str] = None
    ) -> AsyncGenerator[str, None]:
        """Streams text completion asynchronously."""
        logger.info(f"Streaming LLM response using model {self.model_name}")
        # Placeholder generator skeleton
        yield "Streaming chunk placeholder..."
        raise NotImplementedError("LLM stream client to be implemented.")
