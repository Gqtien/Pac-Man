from dataclasses import dataclass, field
from enum import Enum, auto
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

    @property
    def center(self) -> tuple[float, float]:
        return (
            self.pos.x + self.direction.dx * self.progress,
            self.pos.y + self.direction.dy * self.progress,
        )


@dataclass
class Pacman(Entity):
    alive: bool = True
    stall: float = 0.0


class GhostPersonality(Enum):
    BLINKY = auto()
    PINKY = auto()
    INKY = auto()
    CLYDE = auto()


class GhostState(Enum):
    CHASE = auto()
    SCATTER = auto()
    DEAD = auto()
    FRIGHTENED = auto()


@dataclass
class Ghost(Entity):
    personality: GhostPersonality
    home: Vec2
    frightened_timer: float = 0.0
    state: GhostState = GhostState.CHASE
