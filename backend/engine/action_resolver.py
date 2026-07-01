from __future__ import annotations
from models.agent_state import Action, ActionType
from models.world_state import WorldState, WorldEvent


def resolve_action(action: Action, agent, world: WorldState, all_agents: list) -> str | None:
    """Validate and apply an action. Returns a description string, or None if invalid."""

    if action.type == ActionType.MOVE:
        loc = action.target_location
        if loc and loc in world.locations:
            old = agent.state.location
            agent.state.location = loc
            agent.state.energy = max(0, agent.state.energy - 5)
            return f"{agent.name} moved from {old} to {loc}"

    elif action.type == ActionType.TRADE:
        target_name = action.target_agent
        target = next((a for a in all_agents if a.name == target_name), None)
        if not target:
            return None
        if agent.state.location != target.state.location:
            return None

        give_res = action.give_resource
        give_amt = action.give_amount
        want_res = action.want_resource
        want_amt = action.want_amount

        if not give_res or not want_res:
            return None
        if agent.state.inventory.get(give_res, 0) < give_amt:
            return None
        if target.state.inventory.get(want_res, 0) < want_amt:
            return f"{agent.name} tried to trade with {target_name} but {target_name} doesn't have enough {want_res}"

        agent.state.inventory[give_res] = agent.state.inventory.get(give_res, 0) - give_amt
        agent.state.inventory[want_res] = agent.state.inventory.get(want_res, 0) + want_amt
        target.state.inventory[want_res] = target.state.inventory.get(want_res, 0) - want_amt
        target.state.inventory[give_res] = target.state.inventory.get(give_res, 0) + give_amt

        agent.state.update_relationship(target_name, 0.1, "traded")
        target.state.update_relationship(agent.name, 0.1, "traded")

        return f"{agent.name} traded {give_amt} {give_res} for {want_amt} {want_res} with {target_name}"

    elif action.type == ActionType.TALK:
        target_name = action.target_agent
        target = next((a for a in all_agents if a.name == target_name), None)
        if not target:
            return None
        if agent.state.location != target.state.location:
            return None

        msg = action.message or "..."
        agent.state.update_relationship(target_name, 0.05)
        target.state.update_relationship(agent.name, 0.05)

        return f'{agent.name} said to {target_name}: "{msg}"'

    elif action.type == ActionType.GATHER:
        loc = world.locations.get(agent.state.location)
        if not loc:
            return None
        res_name = action.gather_resource
        if not res_name or res_name not in loc.resources:
            return None
        res = loc.resources[res_name]
        if res.quantity <= 0:
            return f"{agent.name} tried to gather {res_name} but none left"

        amount = min(3, res.quantity)
        res.quantity -= amount
        agent.state.inventory[res_name] = agent.state.inventory.get(res_name, 0) + amount
        agent.state.energy = max(0, agent.state.energy - 10)
        return f"{agent.name} gathered {amount} {res_name}"

    elif action.type == ActionType.REST:
        agent.state.energy = min(100, agent.state.energy + 20)
        return f"{agent.name} rested (energy: {agent.state.energy})"

    elif action.type == ActionType.IDLE:
        return f"{agent.name} did nothing"

    return None
