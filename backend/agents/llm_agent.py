from __future__ import annotations
from .base import BaseAgent
from models.agent_state import Action, ActionType
from llm.client import get_agent_decision


class LLMAgent(BaseAgent):
    async def decide(self, perception: dict) -> Action:
        action = await get_agent_decision(
            self.state,
            perception,
            perception.get("tick", 0),
            perception.get("time_of_day", "morning"),
        )
        return action
