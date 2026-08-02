"""
Base Agent Abstract Class.
Defines standard lifecycle and asynchronous execution interface for all sub-agents.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict


class BaseAgent(ABC):
    """Abstract Base Class for AI Agents."""

    def __init__(self, agent_name: str):
        self.agent_name = agent_name

    @abstractmethod
    async def run(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """Runs agent task execution with provided inputs."""
        pass
