from __future__ import annotations
import json
from groq import AsyncGroq
from config import GROQ_API_KEY, GROQ_MODEL
from models.agent_state import Action, ActionType
from .prompts import SYSTEM_PROMPT, build_perception_prompt


_client: AsyncGroq | None = None


def get_client() -> AsyncGroq:
    global _client
    if _client is None:
        _client = AsyncGroq(api_key=GROQ_API_KEY)
    return _client


async def get_agent_decision(agent_state, perception: dict, world_tick: int, time_of_day: str) -> Action:
    client = get_client()
    system = SYSTEM_PROMPT.format(name=agent_state.name, personality=agent_state.personality)
    user_msg = build_perception_prompt(agent_state, perception, world_tick, time_of_day)

    try:
        response = await client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user_msg},
            ],
            temperature=0.8,
            max_tokens=200,
        )
        raw = response.choices[0].message.content.strip()
        return parse_action(raw)
    except Exception as e:
        print(f"  [LLM ERROR for {agent_state.name}]: {e}")
        return Action(type=ActionType.IDLE)


def parse_action(raw: str) -> Action:
    try:
        raw = raw.strip()
        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
        data = json.loads(raw)
    except json.JSONDecodeError:
        return Action(type=ActionType.IDLE)

    action_type = data.get("action", "idle").lower()

    if action_type == "move":
        return Action(type=ActionType.MOVE, target_location=data.get("location"))
    elif action_type == "trade":
        return Action(
            type=ActionType.TRADE,
            target_agent=data.get("target"),
            give_resource=data.get("give"),
            give_amount=data.get("give_amount", 1),
            want_resource=data.get("want"),
            want_amount=data.get("want_amount", 1),
        )
    elif action_type == "talk":
        return Action(
            type=ActionType.TALK,
            target_agent=data.get("target"),
            message=data.get("message", "..."),
        )
    elif action_type == "gather":
        return Action(type=ActionType.GATHER, gather_resource=data.get("resource"))
    elif action_type == "rest":
        return Action(type=ActionType.REST)
    else:
        return Action(type=ActionType.IDLE)
