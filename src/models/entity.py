from dataclasses import dataclass, field
from enum import Enum, auto
from .colors import Color
from .direction import Direction
from .vec import Vec2


@dataclass
class Entity:
    pos: Vec2
    direction: Direction
    dirty: bool = field(default=True, kw_only=True)
    wanted: Direction = field(default=Direction.NONE, kw_only=True)
    progress: float = field(default=0.0, kw_only=True)
    anim_progress: float = field(default=0.0, kw_only=True)


@dataclass
class Pacman(Entity):
    ...


class GhostPersonality(Enum):
    BLINKY = Color.BLINKY
    PINKY = Color.PINKY
    INKY = Color.INKY
    CLYDE = Color.CLYDE


class GhostState(Enum):
    CHASE = auto()
    SCATTER = auto()
    DEAD = auto()
    FRIGHTENED = auto()


@dataclass
class Ghost(Entity):
    personality: GhostPersonality
    state: GhostState = GhostState.CHASE

    @property
    def color(self) -> str:
        return self.personality.value
