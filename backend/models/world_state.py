from __future__ import annotations
from enum import Enum
from pydantic import BaseModel, Field


class LocationType(str, Enum):
    HOUSE = "house"
    MARKET = "market"
    FARM = "farm"
    FOREST = "forest"
    SQUARE = "square"


class Position(BaseModel):
    x: int
    y: int


class Resource(BaseModel):
    type: str
    quantity: int
    regen_rate: int = 0


class Location(BaseModel):
    name: str
    type: LocationType
    position: Position
    resources: dict[str, Resource] = Field(default_factory=dict)
    description: str = ""


class WorldEvent(BaseModel):
    tick: int
    source: str
    event_type: str
    description: str
    targets: list[str] = Field(default_factory=list)


class WorldState(BaseModel):
    tick: int = 0
    time_of_day: str = "morning"
    locations: dict[str, Location] = Field(default_factory=dict)
    events: list[WorldEvent] = Field(default_factory=list)
    recent_events: list[WorldEvent] = Field(default_factory=list)

    def advance_time(self):
        cycle = ["morning", "afternoon", "evening", "night"]
        idx = cycle.index(self.time_of_day)
        self.time_of_day = cycle[(idx + 1) % len(cycle)]

    def get_agents_at(self, location: str, all_agents: list) -> list[str]:
        return [a.state.name for a in all_agents if a.state.location == location]

    def add_event(self, event: WorldEvent):
        self.events.append(event)
        self.recent_events.append(event)
        if len(self.recent_events) > 30:
            self.recent_events.pop(0)

    def regen_resources(self):
        for loc in self.locations.values():
            for res in loc.resources.values():
                if res.regen_rate > 0:
                    res.quantity += res.regen_rate
