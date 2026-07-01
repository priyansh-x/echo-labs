from models.world_state import WorldState, Location, LocationType, Position, Resource
from models.agent_state import AgentState
from agents.llm_agent import LLMAgent
from agents.rule_agent import RuleAgent
from agents.base import BaseAgent


def build_village() -> tuple[WorldState, list[BaseAgent]]:
    locations = {
        "Town Square": Location(
            name="Town Square",
            type=LocationType.SQUARE,
            position=Position(x=2, y=2),
            description="The heart of the village where people gather.",
        ),
        "Market": Location(
            name="Market",
            type=LocationType.MARKET,
            position=Position(x=3, y=1),
            description="A bustling marketplace for trading goods.",
            resources={"gold": Resource(type="gold", quantity=10, regen_rate=2)},
        ),
        "Farm": Location(
            name="Farm",
            type=LocationType.FARM,
            position=Position(x=1, y=3),
            description="Fertile fields for growing food.",
            resources={"food": Resource(type="food", quantity=20, regen_rate=5)},
        ),
        "Forest": Location(
            name="Forest",
            type=LocationType.FOREST,
            position=Position(x=4, y=3),
            description="A dense forest rich in wood.",
            resources={"wood": Resource(type="wood", quantity=25, regen_rate=3)},
        ),
        "Ada's House": Location(
            name="Ada's House",
            type=LocationType.HOUSE,
            position=Position(x=0, y=0),
            description="A well-organized home with ledgers on the desk.",
        ),
        "Boris's House": Location(
            name="Boris's House",
            type=LocationType.HOUSE,
            position=Position(x=4, y=0),
            description="A sturdy house with a locked vault.",
        ),
    }

    world = WorldState(locations=locations)

    agent_configs = [
        {
            "name": "Ada",
            "personality": "You are a sharp, analytical trader. You value fairness and always seek mutually beneficial deals. You keep mental notes of prices and refuse to be cheated. You're respected in the village for your honesty.",
            "location": "Market",
            "inventory": {"gold": 10, "food": 5, "wood": 3},
            "type": "llm",
        },
        {
            "name": "Boris",
            "personality": "You are an aggressive negotiator who always pushes for the best deal. You hoard resources and trust no one fully. You respect strength and cunning. You sometimes lie to get what you want.",
            "location": "Boris's House",
            "inventory": {"gold": 15, "food": 2, "wood": 1},
            "type": "llm",
        },
        {
            "name": "Clara",
            "personality": "You are the social butterfly of the village. You love gossip, making friends, and building alliances. You trade to build relationships, not profit. You remember everything people tell you.",
            "location": "Town Square",
            "inventory": {"gold": 5, "food": 5, "wood": 5},
            "type": "llm",
        },
        {
            "name": "Dmitri",
            "personality": "You are a cautious, hardworking farmer. You prefer self-sufficiency over trading. You're risk-averse and suspicious of smooth talkers. You value routine and stability.",
            "location": "Farm",
            "inventory": {"gold": 3, "food": 15, "wood": 2},
            "type": "rule",
        },
        {
            "name": "Eve",
            "personality": "You are endlessly curious and love exploring. You seek novelty, information, and rare resources. You're friendly but easily bored. You ask lots of questions and wander between locations.",
            "location": "Forest",
            "inventory": {"gold": 8, "food": 8, "wood": 8},
            "type": "llm",
        },
    ]

    agents: list[BaseAgent] = []
    for cfg in agent_configs:
        state = AgentState(
            name=cfg["name"],
            personality=cfg["personality"],
            location=cfg["location"],
            inventory=cfg["inventory"],
        )
        if cfg["type"] == "llm":
            agents.append(LLMAgent(state))
        else:
            agents.append(RuleAgent(state))

    return world, agents
