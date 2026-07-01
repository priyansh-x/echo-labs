from __future__ import annotations
import random
from .base import BaseAgent
from models.agent_state import Action, ActionType


class RuleAgent(BaseAgent):
    async def decide(self, perception: dict) -> Action:
        if self.state.energy < 20:
            return Action(type=ActionType.REST)

        nearby_agents = perception.get("nearby_agents", [])
        available_resources = perception.get("available_resources", {})
        all_locations = perception.get("all_locations", [])

        roll = random.random()

        if roll < 0.25 and nearby_agents:
            target = random.choice(nearby_agents)
            my_resources = {k: v for k, v in self.state.inventory.items() if v > 0}
            if my_resources:
                give_res = random.choice(list(my_resources.keys()))
                want_options = ["food", "wood", "gold"]
                want_res = random.choice([r for r in want_options if r != give_res])
                return Action(
                    type=ActionType.TRADE,
                    target_agent=target,
                    give_resource=give_res,
                    give_amount=random.randint(1, min(3, my_resources[give_res])),
                    want_resource=want_res,
                    want_amount=random.randint(1, 3),
                )

        if roll < 0.45 and nearby_agents:
            target = random.choice(nearby_agents)
            messages = [
                "How's your day going?",
                "The weather is nice today.",
                "Have you seen any good deals at the market?",
                "I've been working hard lately.",
                "Do you need any help with anything?",
            ]
            return Action(
                type=ActionType.TALK,
                target_agent=target,
                message=random.choice(messages),
            )

        if roll < 0.65 and available_resources:
            res_name = random.choice(list(available_resources.keys()))
            return Action(type=ActionType.GATHER, gather_resource=res_name)

        if roll < 0.85 and all_locations:
            other_locations = [l for l in all_locations if l != self.state.location]
            if other_locations:
                return Action(
                    type=ActionType.MOVE,
                    target_location=random.choice(other_locations),
                )

        return Action(type=ActionType.REST)
