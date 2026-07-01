from __future__ import annotations
import asyncio
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from models.world_state import WorldState, WorldEvent
from agents.base import BaseAgent
from .action_resolver import resolve_action

console = Console()


class SimulationEngine:
    def __init__(self, world: WorldState, agents: list[BaseAgent], tick_delay: float = 1.0):
        self.world = world
        self.agents = agents
        self.tick_delay = tick_delay
        self.running = False
        self.snapshots: list[dict] = []

    def build_perception(self, agent: BaseAgent) -> dict:
        loc_name = agent.state.location
        nearby = [
            a.name for a in self.agents
            if a.name != agent.name and a.state.location == loc_name
        ]

        loc = self.world.locations.get(loc_name)
        available_resources = {}
        if loc:
            available_resources = {
                name: res.quantity
                for name, res in loc.resources.items()
                if res.quantity > 0
            }

        recent_events = [
            e.description for e in self.world.recent_events[-10:]
            if agent.name in e.targets or e.source == agent.name or not e.targets
        ]

        return {
            "tick": self.world.tick,
            "time_of_day": self.world.time_of_day,
            "nearby_agents": nearby,
            "available_resources": available_resources,
            "all_locations": list(self.world.locations.keys()),
            "recent_events": recent_events,
        }

    async def run_tick(self):
        self.world.tick += 1
        if self.world.tick % 4 == 0:
            self.world.advance_time()
        if self.world.tick % 8 == 0:
            self.world.regen_resources()

        perceptions = {agent.name: self.build_perception(agent) for agent in self.agents}

        decisions = await asyncio.gather(*[
            agent.decide(perceptions[agent.name]) for agent in self.agents
        ])

        tick_events: list[str] = []
        for agent, action in zip(self.agents, decisions):
            result = resolve_action(action, agent, self.world, self.agents)
            if result:
                tick_events.append(result)
                event = WorldEvent(
                    tick=self.world.tick,
                    source=agent.name,
                    event_type=action.type.value,
                    description=result,
                    targets=[action.target_agent] if action.target_agent else [],
                )
                self.world.add_event(event)
                for a in self.agents:
                    if a.name == agent.name or (action.target_agent and a.name == action.target_agent):
                        importance = 0.8 if action.type.value in ("trade", "talk") else 0.4
                        a.record_event(self.world.tick, result, importance)

        self.render_tick(tick_events)

        if self.world.tick % 10 == 0:
            self.snapshots.append({
                "tick": self.world.tick,
                "world": self.world.model_dump(),
                "agents": [a.state.model_dump() for a in self.agents],
            })

    def render_tick(self, events: list[str]):
        header = f"[bold cyan]═══ Tick {self.world.tick} | {self.world.time_of_day.upper()} ═══[/bold cyan]"
        console.print(header)

        if events:
            for evt in events:
                console.print(f"  {evt}")
        else:
            console.print("  [dim]Nothing happened.[/dim]")
        console.print()

    def render_status(self):
        table = Table(title="Village Status", show_header=True)
        table.add_column("Agent", style="bold")
        table.add_column("Location")
        table.add_column("Energy")
        table.add_column("Inventory")
        table.add_column("Key Relationships")

        for agent in self.agents:
            inv = ", ".join(f"{v}{k[0].upper()}" for k, v in agent.state.inventory.items() if v > 0) or "-"
            rels = ", ".join(
                f"{n}({r.score:+.1f})"
                for n, r in agent.state.relationships.items()
                if abs(r.score) > 0.2
            ) or "-"
            table.add_row(
                agent.name,
                agent.state.location,
                f"{agent.state.energy}/100",
                inv,
                rels,
            )
        console.print(table)
        console.print()

    async def run(self, max_ticks: int = 200):
        self.running = True
        console.print(Panel("[bold green]Echo Labs Simulation Starting[/bold green]", expand=False))
        self.render_status()

        try:
            for _ in range(max_ticks):
                if not self.running:
                    break
                await self.run_tick()
                if self.world.tick % 10 == 0:
                    self.render_status()
                await asyncio.sleep(self.tick_delay)
        except KeyboardInterrupt:
            console.print("\n[yellow]Simulation paused by user.[/yellow]")

        console.print(Panel("[bold red]Simulation Ended[/bold red]", expand=False))
        self.render_status()
