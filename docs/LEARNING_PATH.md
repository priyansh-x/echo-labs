# Echo Labs — Learning Path

This document maps out what you'll learn by building each part of Echo Labs, and the order to build things in.

---

## Phase 1: The Engine (Weeks 1-2)

### What you're building
A Python simulation engine that runs a simple village world with 5 agents in the terminal.

### What you'll learn
- **Async Python** (asyncio, gather, tasks) — the engine runs agents in parallel
- **State machines** — the tick loop is a state machine
- **Abstract classes** — designing the Agent interface so LLM and rule-based agents share it
- **Prompt engineering** — crafting prompts that make agents behave realistically
- **API integration** — calling Claude's API, handling responses, managing rate limits

### Key concepts to understand first
1. What is `async/await` and why do we need it? (agents make API calls — we don't want to wait one-by-one)
2. What is an abstract base class in Python?
3. How does a game loop work? (our tick loop is essentially a game loop)

### Milestone
Run `python -m engine.run` and watch 5 agents trade, talk, and form opinions in your terminal.

---

## Phase 2: The API Layer (Week 3)

### What you're building
A FastAPI server that wraps the engine and exposes it via REST + WebSocket.

### What you'll learn
- **REST API design** — resource-based URLs, HTTP methods, status codes
- **WebSocket protocol** — persistent connections, event-driven communication
- **FastAPI** — dependency injection, Pydantic models, async endpoints
- **Database basics** — SQLAlchemy, migrations with Alembic

### Key concepts to understand first
1. What's the difference between REST and WebSocket? When do you use each?
2. What is Pydantic and why is it useful?
3. What is an ORM and why use one?

### Milestone
Open `http://localhost:8000/docs` and see your API. Start a simulation via POST request. Connect via WebSocket and receive live tick updates.

---

## Phase 3: The Frontend Shell (Week 4)

### What you're building
A Next.js app with a dashboard, simulation viewer (2D first), and basic controls.

### What you'll learn
- **Next.js App Router** — layouts, pages, server vs client components
- **React state management** — Zustand for global state
- **WebSocket in React** — connecting, reconnecting, handling events
- **Component architecture** — how to split a complex UI into reusable pieces

### Key concepts to understand first
1. What's the difference between server and client components in Next.js?
2. What is Zustand and how does it compare to useState/useContext?
3. What is a WebSocket and how does it differ from HTTP?

### Milestone
A working dashboard that shows a running simulation as a text feed + simple 2D canvas with dots representing agents.

---

## Phase 4: 3D World (Weeks 5-6)

### What you're building
Replace the 2D canvas with a 3D scene using React Three Fiber.

### What you'll learn
- **Three.js fundamentals** — scenes, cameras, meshes, materials, lighting
- **React Three Fiber** — declarative 3D in React
- **3D math basics** — vectors, rotations, camera controls
- **Performance** — instancing, LOD, frame budgets
- **Shaders** (optional) — custom visual effects

### Key concepts to understand first
1. What is a scene graph?
2. How does a perspective camera work?
3. What is a mesh (geometry + material)?

### Milestone
A 3D village scene with terrain, agent characters walking around, buildings, and a day/night cycle.

---

## Phase 5: Agent Inspector (Week 7)

### What you're building
Click any agent in the 3D world to see their memory, personality, decision traces, and conversation history.

### What you'll learn
- **UI/UX design** — information-dense panels, progressive disclosure
- **Data visualization** — relationship graphs (D3 or visx), memory timelines
- **React patterns** — compound components, render props, context for selected state

### Milestone
Click an agent → see their personality, last 10 decisions with reasoning, memory entries, and a graph of relationships.

---

## Phase 6: Time Controls & Intervention (Week 8)

### What you're building
Play/pause/speed controls, timeline scrubber for replay, and intervention tools (inject events, modify agents mid-simulation).

### What you'll learn
- **Snapshot/restore patterns** — saving and loading world state
- **Optimistic UI** — responding to user actions before server confirms
- **Event sourcing concepts** — rebuilding state from a sequence of events

### Milestone
Pause a simulation, scrub back 50 ticks, inject "a storm destroys the market", resume, and watch agents react.

---

## Concepts You'll Master By The End

| Concept | Where you'll use it |
|---------|-------------------|
| Async programming | Simulation engine, API calls |
| WebSocket real-time | Engine ↔ Frontend communication |
| State management | Zustand, world state, snapshots |
| 3D graphics | Three.js world visualization |
| API design | REST + WebSocket protocol |
| Database design | PostgreSQL schema, queries |
| Prompt engineering | Agent decision-making |
| System design | How all pieces fit together |
| TypeScript | Frontend type safety |
| Python OOP | Engine, agents, world |

---

## How to Use This Document

Before starting each phase:
1. Read the "key concepts to understand first" section
2. Google/YouTube those concepts if unfamiliar (don't skip this!)
3. Try to write the core logic yourself before asking for help
4. When stuck, ask for **explanation** first, not code
5. After getting it working, refactor to make it clean

The goal is NOT to finish fast. The goal is to understand deeply.
