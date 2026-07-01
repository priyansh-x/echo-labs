# Phase 1: Building the Simulation Engine

This is your first build phase. By the end, you'll have AI agents living in a terminal-based village.

---

## What We're Building

A Python simulation engine with:
- A tick-based world loop
- 5 agents with distinct personalities
- A simple village economy (trading, talking, moving)
- Agent memory and decision-making via Claude API
- Terminal output showing what's happening

## File Structure

```
backend/
├── engine/
│   ├── __init__.py
│   ├── simulation.py      # The main tick loop (YOU WRITE THIS)
│   ├── world.py            # World state management (YOU WRITE THIS)
│   └── action_resolver.py  # Validates & applies agent actions
│
├── agents/
│   ├── __init__.py
│   ├── base.py             # Abstract Agent class (YOU WRITE THIS)
│   ├── llm_agent.py        # LLM-powered agent
│   └── rule_agent.py       # Rule-based agent (YOU WRITE THIS)
│
├── llm/
│   ├── __init__.py
│   ├── client.py           # Claude API wrapper
│   └── prompts.py          # Prompt templates
│
├── models/
│   ├── __init__.py
│   ├── world_state.py      # Pydantic models for world
│   └── agent_state.py      # Pydantic models for agents
│
├── config.py               # Configuration
├── main.py                 # Entry point
└── requirements.txt
```

## Step-by-Step Build Order

### Step 1: Define the Data Models (Start here)

Before writing any logic, define what the world looks like as data.

**Your task**: Create Pydantic models for:
- `Position` (x, y coordinates)
- `Resource` (type, quantity)
- `AgentState` (name, position, inventory, energy, relationships)
- `WorldState` (map size, agents, resources, time_of_day, tick)

Think about: What is the minimum data needed to fully describe the world at any moment?

### Step 2: The Agent Interface

**Your task**: Create an abstract base class `Agent` with:
- Properties: `id`, `name`, `state`
- Abstract method: `async decide(perception: dict) -> Action`
- Method: `update_memory(event: Event)`

Think about: What do ALL agents (LLM, rule-based, hybrid) need in common?

### Step 3: A Simple Rule-Based Agent

**Your task**: Implement a rule-based agent that:
- Moves randomly
- Trades if another agent is nearby
- Rests when energy is low

This is your test harness — you can run the simulation without burning API credits.

### Step 4: The Tick Loop

**Your task**: Write the main simulation loop:
```python
async def run_tick(self):
    # Build perceptions for all agents
    # Get decisions from all agents (in parallel!)
    # Resolve conflicts
    # Apply changes to world
    # Log what happened
```

### Step 5: Wire It Up

**Your task**: Create `main.py` that:
- Creates a world with 5 agents
- Runs the tick loop
- Prints what happens each tick to the terminal

### Step 6: Add the LLM Agent

Now replace one rule-based agent with an LLM agent:
- Build the perception → prompt pipeline
- Call Claude API
- Parse the response into an Action
- Handle errors gracefully

---

## The Village World

For Phase 1, our world is a simple village:

```
┌─────────────────────────────────────┐
│           ECHO VILLAGE               │
│                                      │
│   🏠 House    🏪 Market   🌾 Farm   │
│                                      │
│   🏠 House    ⛪ Square   🌾 Farm   │
│                                      │
│   🏠 House    🏪 Market   🌳 Forest │
│                                      │
└─────────────────────────────────────┘
```

**Locations**: Houses, Market, Farm, Forest, Town Square
**Resources**: Food, Wood, Gold
**Actions agents can take**:
- `move(location)` — walk to a location
- `trade(agent, give, receive)` — exchange resources
- `talk(agent, message)` — say something to another agent
- `gather(resource)` — collect resources from the environment
- `rest()` — recover energy

## Agent Personalities (Phase 1)

| Agent | Personality | Initial Resources |
|-------|------------|-------------------|
| Ada | Analytical trader, optimizes for fairness | 10 gold, 5 food |
| Boris | Aggressive negotiator, hoards resources | 15 gold, 2 food |
| Clara | Social connector, gossips, builds alliances | 5 gold, 5 food |
| Dmitri | Cautious farmer, risk-averse, self-sufficient | 3 gold, 15 food |
| Eve | Curious explorer, seeks novelty and information | 8 gold, 8 food |

---

## Success Criteria

You've completed Phase 1 when:
- [ ] Running `python main.py` starts a simulation
- [ ] 5 agents make decisions each tick
- [ ] Agents can move, trade, talk, gather, and rest
- [ ] At least one agent is LLM-powered
- [ ] The terminal shows a readable log of events
- [ ] The simulation runs for 50+ ticks without crashing
- [ ] Agent memory persists across ticks (they remember past events)
