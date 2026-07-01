# Echo Labs

Multi-agent simulation platform — LLM-powered agents in persistent 3D worlds.

## Project structure
- `frontend/` — Next.js 14 + React Three Fiber
- `backend/` — Python FastAPI + simulation engine
- `docs/` — Architecture and learning documentation
- `shared/` — Shared types/schemas

## Key principles
- This is a learning project. Explain architecture decisions before writing code.
- User (Priyansh) writes core logic by hand. Claude helps with boilerplate, debugging, and complex integrations.
- Start simple (terminal), add layers (API, 2D, 3D) incrementally.

## Tech stack
- Frontend: Next.js 14, React 18, TypeScript, React Three Fiber, Zustand, Socket.IO client
- Backend: Python 3.12+, FastAPI, SQLAlchemy, Alembic, Socket.IO
- LLM: Claude API (Anthropic SDK)
- DB: PostgreSQL + Redis
- 3D: Three.js via React Three Fiber

## Commands
- Backend: `cd backend && uvicorn main:app --reload`
- Frontend: `cd frontend && npm run dev`
- Tests: `cd backend && pytest` / `cd frontend && npm test`
