from __future__ import annotations
from enum import Enum
from pydantic import BaseModel, Field


class ActionType(str, Enum):
    MOVE = "move"
    TRADE = "trade"
    TALK = "talk"
    GATHER = "gather"
    REST = "rest"
    IDLE = "idle"


class Action(BaseModel):
    type: ActionType
    target_location: str | None = None
    target_agent: str | None = None
    message: str | None = None
    give_resource: str | None = None
    give_amount: int = 0
    want_resource: str | None = None
    want_amount: int = 0
    gather_resource: str | None = None


class Relationship(BaseModel):
    agent_name: str
    score: float = Field(default=0.0, ge=-1.0, le=1.0)
    notes: str = ""


class MemoryEntry(BaseModel):
    tick: int
    content: str
    importance: float = Field(default=0.5, ge=0.0, le=1.0)


class AgentState(BaseModel):
    name: str
    personality: str
    location: str
    inventory: dict[str, int] = Field(default_factory=dict)
    energy: int = 100
    relationships: dict[str, Relationship] = Field(default_factory=dict)
    short_term_memory: list[MemoryEntry] = Field(default_factory=list)
    long_term_memory: list[MemoryEntry] = Field(default_factory=list)
    max_short_term: int = 15

    def add_memory(self, tick: int, content: str, importance: float = 0.5):
        entry = MemoryEntry(tick=tick, content=content, importance=importance)
        self.short_term_memory.append(entry)
        if len(self.short_term_memory) > self.max_short_term:
            oldest = self.short_term_memory.pop(0)
            if oldest.importance >= 0.7:
                self.long_term_memory.append(oldest)

    def update_relationship(self, agent_name: str, delta: float, note: str = ""):
        if agent_name not in self.relationships:
            self.relationships[agent_name] = Relationship(agent_name=agent_name)
        rel = self.relationships[agent_name]
        rel.score = max(-1.0, min(1.0, rel.score + delta))
        if note:
            rel.notes = note
