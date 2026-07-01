# 🧪 Echo Labs

**A web-based simulation laboratory for creating, running, and experimenting with persistent multi-agent worlds powered by LLMs.**

Watch AI agents live, trade, gossip, form alliances, and evolve — in real-time 3D. Pause the world. Intervene. Rewind. Ask "what if?" and get answers.

![Status](https://img.shields.io/badge/status-early%20development-orange)
![License](https://img.shields.io/badge/license-MIT-blue)

---

## What is Echo Labs?

Echo Labs is an interactive platform where users can:

- **Build worlds** — define environments, resources, rules, and spawn diverse AI agents
- **Watch emergence** — observe agents interact, form relationships, make decisions, and create unexpected outcomes
- **Intervene** — pause simulations, inject events, modify agent traits, and see how the world responds
- **Experiment** — run counterfactuals, compare scenarios, and analyze emergent behaviors scientifically
- **Collaborate** — build and explore simulations together in real-time
- **Share & reproduce** — fork simulations, share discoveries, and reproduce results with full provenance

## Architecture Overview

```
┌─────────────────────────────────────────────────┐
│                  Frontend (Next.js)              │
│  ┌───────────┐ ┌───────────┐ ┌────────────────┐ │
│  │ 3D World  │ │ Dashboard │ │ Agent Inspector │ │
│  │ (Three.js)│ │  & Controls│ │ & Debugger     │ │
│  └───────────┘ └───────────┘ └────────────────┘ │
└──────────────────────┬──────────────────────────┘
                       │ WebSocket + REST
┌──────────────────────┴──────────────────────────┐
│              Backend (FastAPI + Python)           │
│  ┌───────────┐ ┌───────────┐ ┌────────────────┐ │
│  │Simulation │ │  Agent    │ │  World State   │ │
│  │  Engine   │ │  Manager  │ │  & Persistence │ │
│  └───────────┘ └───────────┘ └────────────────┘ │
└──────────────────────┬──────────────────────────┘
                       │
┌──────────────────────┴──────────────────────────┐
│         LLM Layer (Claude API / Others)          │
│         Database (PostgreSQL + Redis)            │
└─────────────────────────────────────────────────┘
```

## Tech Stack

| Layer | Technology | Why |
|-------|-----------|-----|
| Frontend | Next.js 14 + React 18 | Server components, great DX |
| 3D Visualization | Three.js + React Three Fiber | Declarative 3D in React |
| Real-time | WebSockets (Socket.IO) | Bi-directional sim updates |
| Backend | Python + FastAPI | Async-first, great for LLM orchestration |
| Simulation Engine | Custom Python | Turn-based with configurable tick rates |
| LLM | Claude API (Anthropic) | Best reasoning for agent behaviors |
| Database | PostgreSQL | World state, agent memory, sim history |
| Cache/Pub-Sub | Redis | Real-time state, message queues |
| Auth | NextAuth.js | Simple, extensible auth |

## Project Structure

```
echo-labs/
├── frontend/          # Next.js application
│   ├── app/           # App router pages
│   ├── components/    # React components
│   │   ├── world/     # 3D world visualization
│   │   ├── dashboard/ # Dashboard & controls
│   │   └── inspector/ # Agent inspector
│   ├── lib/           # Utilities, API client, stores
│   └── public/        # Static assets
│
├── backend/           # FastAPI application
│   ├── api/           # REST + WebSocket endpoints
│   ├── engine/        # Simulation engine core
│   ├── agents/        # Agent types & behaviors
│   ├── world/         # World state management
│   ├── llm/           # LLM integration layer
│   └── db/            # Database models & migrations
│
├── docs/              # Architecture & learning docs
├── shared/            # Shared types/schemas
└── docker/            # Docker configs
```

## Getting Started

> 🚧 Echo Labs is in early development. Setup instructions coming soon.

```bash
# Clone the repo
git clone https://github.com/priyansh-x/echo-labs.git
cd echo-labs

# Backend
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload

# Frontend
cd frontend
npm install
npm run dev
```

## Development Phases

- [x] **Phase 0** — Project setup, architecture, documentation
- [ ] **Phase 1** — Core simulation engine + basic village world (5-8 agents)
- [ ] **Phase 2** — 3D visualization + agent inspector + timeline controls
- [ ] **Phase 3** — World builder + experiment tools + sharing
- [ ] **Phase 4** — Real-time collaboration + community features

## Contributing

Echo Labs is a learning-driven project. Contributions, ideas, and feedback are welcome!

## License

MIT License — see [LICENSE](LICENSE) for details.
