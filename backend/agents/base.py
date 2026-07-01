from __future__ import annotations
from abc import ABC, abstractmethod
from models.agent_state import AgentState, Action


class BaseAgent(ABC):
    def __init__(self, state: AgentState):
        self.state = state

    @property
    def name(self) -> str:
        return self.state.name

    @property
    def location(self) -> str:
        return self.state.location

    @abstractmethod
    async def decide(self, perception: dict) -> Action:
        ...

    def record_event(self, tick: int, content: str, importance: float = 0.5):
        self.state.add_memory(tick, content, importance)
