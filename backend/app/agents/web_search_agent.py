"""
Web Search Agent.
Responsible for formulating web search queries and gathering raw company information.
"""

from typing import Any, Dict
from app.agents.base import BaseAgent


class WebSearchAgent(BaseAgent):
    """Agent that performs targeted web searches for company data."""

    def __init__(self):
        super().__init__(agent_name="WebSearchAgent")

    async def run(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """Formulates queries and fetches search result content."""
        # Placeholder skeleton
        raise NotImplementedError("WebSearchAgent logic to be implemented.")
