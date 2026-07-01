import asyncio
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from config import GROQ_API_KEY, TICK_DELAY, MAX_TICKS
from engine.simulation import SimulationEngine
from engine.world_builder import build_village
from rich.console import Console

console = Console()


async def main():
    if not GROQ_API_KEY:
        console.print("[bold red]Error:[/bold red] GROQ_API_KEY not set.")
        console.print("Create a .env file with: GROQ_API_KEY=your_key_here")
        console.print("Get a free key at: https://console.groq.com/keys")
        return

    console.print("[bold]Building Echo Village...[/bold]")
    world, agents = build_village()
    console.print(f"Created {len(agents)} agents in {len(world.locations)} locations.\n")

    engine = SimulationEngine(world, agents, tick_delay=TICK_DELAY)
    await engine.run(max_ticks=MAX_TICKS)


if __name__ == "__main__":
    asyncio.run(main())
