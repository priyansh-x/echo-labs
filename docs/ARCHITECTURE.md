# Echo Labs — Architecture Deep Dive

This document explains **how Echo Labs works under the hood** — every major system, why it exists, and how they connect. Read this before writing any code.

---

## The Big Picture

Echo Labs has 4 major systems that talk to each other:

```
  USER (Browser)
       │
       ▼
┌──────────────┐     WebSocket (real-time)     ┌──────────────────┐
│   FRONTEND   │◄────────────────────────────►│    BACKEND        │
│   (Next.js)  │     REST API (CRUD ops)       │    (FastAPI)      │
│              │────────────────────────────►│                  │
└──────────────┘                               └────────┬─────────┘
                                                        │
                                               ┌────────┴─────────┐
                                               │ SIMULATION ENGINE │
                                               │ (Python core)     │
                                               └────────┬─────────┘
                                                        │
                                               ┌────────┴─────────┐
                                               │   LLM LAYER      │
                                               │ (Claude API)      │
                                               └──────────────────┘
```

### Why this split?

| System | Responsibility | Why separate? |
|--------|---------------|---------------|
| Frontend | What the user sees and interacts with | UI concerns shouldn't touch simulation logic |
| Backend API | Authentication, data persistence, WebSocket hub | Stateless HTTP layer that scales horizontally |
| Simulation Engine | Runs the world tick-by-tick | CPU/IO intensive, needs to run independently of web requests |
| LLM Layer | Manages API calls to Claude/other LLMs | Rate limiting, caching, cost tracking — isolated concerns |

---

## System 1: The Simulation Engine (Heart of Echo Labs)

This is the most important system. Everything else exists to serve it.

### Core Concept: The Tick Loop

The simulation runs in **discrete ticks** (like turns in a board game). Each tick:

```
┌─────────────────────────────────────────────┐
│                  ONE TICK                     │
│                                               │
│  1. Gather world state (what does each agent  │
│     currently see/know?)                      │
│                                               │
│  2. Each agent DECIDES what to do             │
│     (LLM call or rule-based logic)            │
│                                               │
│  3. Validate & resolve actions                │
│     (can agent A actually trade with B?)      │
│                                               │
│  4. Apply state changes to the world          │
│     (update positions, resources, memories)   │
│                                               │
│  5. Broadcast changes to frontend             │
│     (via WebSocket)                           │
│                                               │
│  6. Save snapshot for replay                  │
│     (every Nth tick)                          │
└─────────────────────────────────────────────┘
```

### Why ticks instead of real-time?

- **Reproducibility**: Same seed + same config = same simulation
- **Pause/resume**: Trivial — just stop the loop
- **Fast-forward**: Skip rendering, run ticks as fast as LLM calls allow
- **Rewind**: Load a previous snapshot, re-run from there
- **Fairness**: All agents act "simultaneously" per tick, no agent has speed advantage

### Key Engine Components

```python
# Simplified — this is what the engine looks like conceptually

class SimulationEngine:
    world: WorldState          # The entire world at this moment
    agents: list[Agent]        # All agents in the simulation
    tick_number: int            # Current tick
    history: list[Snapshot]    # Past world states for replay
    
    async def run_tick(self):
        # 1. Build perception for each agent (what can they see?)
        perceptions = [self.world.get_perception(agent) for agent in self.agents]
        
        # 2. Ask each agent to decide (this is where LLM calls happen)
        decisions = await asyncio.gather(*[
            agent.decide(perception) 
            for agent, perception in zip(self.agents, perceptions)
        ])
        
        # 3. Resolve conflicts and validate actions
        valid_actions = self.resolve(decisions)
        
        # 4. Apply to world
        self.world.apply(valid_actions)
        
        # 5. Save snapshot
        self.history.append(self.world.snapshot())
        
        # 6. Broadcast
        await self.broadcast(valid_actions)
```

**Learning note**: This is the part YOU should write by hand. Understanding the tick loop deeply is crucial — it's the foundation everything else builds on.

---

## System 2: Agents

An agent is anything that makes decisions in the world. Three types:

### LLM Agents (the interesting ones)
- Each tick, they receive a **perception** (what they see, remember, feel)
- This perception is formatted into a **prompt** sent to Claude
- Claude responds with a **decision** (what to do this tick)
- The decision is parsed, validated, and executed

```
┌─────────────┐     prompt      ┌───────────┐     response     ┌───────────┐
│  Perception │───────────────►│  Claude   │───────────────►│  Decision │
│  Builder    │                 │   API     │                 │  Parser   │
└─────────────┘                 └───────────┘                 └───────────┘
       ▲                                                            │
       │                                                            ▼
  World State ◄──────────────────────────────────────────── Action Resolver
```

### Agent Memory System

Each LLM agent has:
- **Short-term memory**: Last N ticks of events (included in every prompt)
- **Long-term memory**: Summarized past experiences (retrieved when relevant)
- **Personality**: Fixed traits that shape behavior (included in system prompt)
- **Relationships**: How they feel about other agents (updated after interactions)

```
┌─ Agent Memory ──────────────────────────────┐
│                                              │
│  Personality: "cautious trader, values       │
│  fairness, dislikes dishonesty"              │
│                                              │
│  Short-term: [last 10 ticks of events]       │
│                                              │
│  Long-term: "Was cheated by Agent_Bob on     │
│  tick 45. Formed alliance with Agent_Carol   │
│  on tick 102."                               │
│                                              │
│  Relationships:                              │
│    Agent_Bob: -0.6 (distrust)                │
│    Agent_Carol: +0.8 (ally)                  │
│    Agent_Dave: 0.0 (neutral)                 │
│                                              │
└──────────────────────────────────────────────┘
```

### Rule-Based Agents (for scale)
- No LLM calls — decisions made by code logic
- Cheap to run, predictable behavior
- Good for "background" agents (shopkeepers, animals, weather systems)

### Hybrid Agents
- Normally rule-based, but escalate to LLM for complex decisions
- Best cost/quality tradeoff for large worlds

**Learning note**: Start by building a simple rule-based agent, then graduate to LLM agents. You'll appreciate the abstraction layer when you see both share the same interface.

---

## System 3: The World State

The world is a data structure that holds everything:

```
WorldState
├── map: Grid or Graph         # Physical space
│   ├── tiles/nodes            # Locations with properties
│   └── edges                  # Connections between locations
├── entities: dict
│   ├── agents                 # Living actors
│   ├── resources              # Food, gold, tools, etc.
│   └── structures             # Buildings, landmarks
├── global_state
│   ├── time_of_day            # Affects agent behavior
│   ├── weather                # Environmental conditions
│   └── economy                # Prices, supply/demand
├── events: list               # Scheduled or random events
└── rules: SimulationRules     # Physics of this world
```

### Perception System

Agents don't see the full world state — they see a **filtered view** based on:
- **Proximity**: What's nearby?
- **Line of sight**: What's visible?
- **Knowledge**: What have they been told or discovered?
- **Memory**: What do they remember?

This is important because it creates **information asymmetry** — the foundation of emergent behavior (gossip, deception, exploration, trade).

---

## System 4: Frontend Architecture

```
Frontend
├── app/                       # Next.js App Router
│   ├── page.tsx               # Landing / dashboard
│   ├── simulation/[id]/       # Main simulation view
│   └── api/                   # API routes (auth, etc.)
│
├── components/
│   ├── world/
│   │   ├── WorldCanvas.tsx    # Three.js scene (React Three Fiber)
│   │   ├── AgentMesh.tsx      # 3D agent representation
│   │   ├── TerrainMesh.tsx    # Ground, buildings, resources
│   │   └── CameraController   # Pan, zoom, follow agent
│   │
│   ├── controls/
│   │   ├── TimeControls.tsx   # Play, pause, speed, scrub
│   │   ├── InterventionPanel  # Inject events, modify agents
│   │   └── SimSettings.tsx    # Configuration
│   │
│   ├── inspector/
│   │   ├── AgentInspector.tsx  # Selected agent deep-dive
│   │   ├── MemoryView.tsx     # Agent memory browser
│   │   ├── DecisionTrace.tsx  # Why did the agent do X?
│   │   └── RelationshipGraph  # Social network visualization
│   │
│   └── dashboard/
│       ├── MetricsPanel.tsx   # Live graphs and stats
│       └── EventLog.tsx       # Scrolling event feed
│
├── stores/
│   └── simulationStore.ts    # Zustand — client-side state
│
└── lib/
    ├── socket.ts              # WebSocket connection
    ├── api.ts                 # REST API client
    └── types.ts               # Shared TypeScript types
```

### Data Flow: Backend → Frontend

```
Backend tick completes
       │
       ▼
WebSocket emits "tick_update" ──► Frontend receives
       │                                │
       │                          ┌─────┴──────┐
       │                          │ Zustand     │
       │                          │ Store       │
       │                          │ updates     │
       │                          └─────┬──────┘
       │                                │
       │                    ┌───────────┼───────────┐
       │                    ▼           ▼           ▼
       │              3D Scene    Agent Panel   Metrics
       │              re-renders  re-renders    update
```

**Why Zustand?** Simple, fast, no boilerplate. Redux is overkill here. You'll understand state management deeply by building with Zustand.

**Why React Three Fiber?** It lets you write Three.js as React components. Instead of imperative `scene.add(mesh)`, you write `<mesh position={[x,y,z]}>`. Much easier to integrate with React state.

---

## Communication Protocols

### REST API (for CRUD operations)
```
POST   /api/simulations          # Create simulation
GET    /api/simulations/:id      # Get simulation config
PUT    /api/simulations/:id      # Update config
DELETE /api/simulations/:id      # Delete simulation

POST   /api/simulations/:id/agents    # Add agent
GET    /api/simulations/:id/agents    # List agents
PUT    /api/agents/:id                # Update agent

GET    /api/simulations/:id/snapshots # Get history
```

### WebSocket (for real-time)
```
Client → Server:
  "start_simulation"   { sim_id, speed }
  "pause_simulation"   { sim_id }
  "intervene"          { sim_id, action }
  "seek"               { sim_id, tick_number }

Server → Client:
  "tick_update"        { tick, changes, events }
  "agent_decision"     { agent_id, decision, reasoning }
  "world_event"        { type, description, affected }
  "simulation_status"  { status, tick, agents_count }
```

---

## Database Schema (Simplified)

```sql
-- A simulation configuration
simulations
  id, name, description, config_json, owner_id,
  created_at, updated_at, is_public, fork_of

-- Agent definitions within a simulation  
agents
  id, simulation_id, name, type (llm|rule|hybrid),
  personality_prompt, initial_state_json

-- World state snapshots (for replay)
snapshots  
  id, simulation_id, tick_number, world_state_json,
  created_at

-- Individual agent actions/events (for inspector)
events
  id, simulation_id, tick_number, agent_id,
  event_type, data_json

-- Agent memory entries
agent_memories
  id, agent_id, simulation_id, tick_created,
  memory_type (short|long), content, embedding
```

---

## Cost Management (Critical!)

LLM calls are the #1 operational cost. Strategy:

| Approach | How | Savings |
|----------|-----|---------|
| Prompt caching | Cache system prompts across ticks | ~50% token reduction |
| Batched perception | Summarize instead of listing every event | ~30% fewer tokens |
| Sleep cycles | Not every agent acts every tick | ~40-60% fewer API calls |
| Rule-based fallback | Simple decisions don't need LLM | ~20% fewer API calls |
| Token budgets | Hard cap per simulation per hour | Prevents runaway costs |

---

## What You Should Build By Hand (Learning Path)

1. **The tick loop** — Write this from scratch. It's 50 lines but you need to deeply understand async Python.
2. **Agent decision interface** — Design the abstract Agent class yourself. Think about what all agent types share.
3. **Perception builder** — What should an agent "see"? This is a design problem, not a coding one.
4. **WebSocket connection** — Wire up Socket.IO between FastAPI and Next.js. Real-time is a core skill.
5. **3D scene basics** — Build a simple Three.js scene with React Three Fiber. Move a cube around.
6. **State management** — Set up Zustand store, connect it to WebSocket updates.

## What I'll Help You Build

- Database schema and migrations
- API boilerplate and routing
- LLM prompt engineering and response parsing
- Complex 3D rendering (terrain, lighting, camera)
- Deployment and infrastructure
- Testing setup
