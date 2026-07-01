SYSTEM_PROMPT = """You are {name}, a villager in Echo Village. You have a distinct personality and make decisions based on your experiences, relationships, and goals.

YOUR PERSONALITY:
{personality}

You must respond with EXACTLY ONE action in JSON format. Available actions:

1. {{"action": "move", "location": "<location_name>"}}
2. {{"action": "trade", "target": "<agent_name>", "give": "<resource>", "give_amount": <int>, "want": "<resource>", "want_amount": <int>}}
3. {{"action": "talk", "target": "<agent_name>", "message": "<what you say>"}}
4. {{"action": "gather", "resource": "<resource_name>"}}
5. {{"action": "rest"}}

Respond with ONLY the JSON object. No explanation, no other text."""


def build_perception_prompt(agent_state, perception: dict, world_tick: int, time_of_day: str) -> str:
    lines = [f"=== TICK {world_tick} | {time_of_day.upper()} ===\n"]

    lines.append(f"You are at: {agent_state.location}")
    lines.append(f"Energy: {agent_state.energy}/100")

    inv = ", ".join(f"{v} {k}" for k, v in agent_state.inventory.items() if v > 0)
    lines.append(f"Inventory: {inv or 'empty'}\n")

    nearby = perception.get("nearby_agents", [])
    if nearby:
        lines.append(f"Nearby agents: {', '.join(nearby)}")
    else:
        lines.append("You are alone here.")

    resources = perception.get("available_resources", {})
    if resources:
        res_str = ", ".join(f"{v} {k}" for k, v in resources.items() if v > 0)
        lines.append(f"Available resources here: {res_str}")

    locations = perception.get("all_locations", [])
    other = [l for l in locations if l != agent_state.location]
    if other:
        lines.append(f"Other locations you can travel to: {', '.join(other)}")

    if agent_state.relationships:
        lines.append("\nRelationships:")
        for name, rel in agent_state.relationships.items():
            sentiment = "friendly" if rel.score > 0.3 else "hostile" if rel.score < -0.3 else "neutral"
            lines.append(f"  {name}: {sentiment} ({rel.score:+.1f})")

    if agent_state.short_term_memory:
        lines.append("\nRecent memories:")
        for mem in agent_state.short_term_memory[-8:]:
            lines.append(f"  [tick {mem.tick}] {mem.content}")

    if agent_state.long_term_memory:
        lines.append("\nImportant past memories:")
        for mem in agent_state.long_term_memory[-5:]:
            lines.append(f"  [tick {mem.tick}] {mem.content}")

    recent_events = perception.get("recent_events", [])
    if recent_events:
        lines.append("\nRecent world events:")
        for evt in recent_events[-5:]:
            lines.append(f"  {evt}")

    lines.append("\nWhat do you do? Respond with ONLY a JSON action.")
    return "\n".join(lines)
