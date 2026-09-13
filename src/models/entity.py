from dataclasses import dataclass, field
from enum import Enum, auto
from .direction import Direction
from .colors import Color
from .vec import Vec2


class Personality(Enum):
    BLINKY = Color.RED
    PINKY = Color.PINK
    INKY = Color.CYAN
    CLYDE = Color.ORANGE


class State(Enum):
    CHASE = auto()
    SCATTER = auto()
    DEAD = auto()
    FRIGHTENED = auto()


@dataclass
class Entity:
    pos: Vec2
    direction: Direction
    movement_progress: float = field(default=0.0, kw_only=True)


@dataclass
class Pacman(Entity): ...


@dataclass
class Ghost(Entity):
    personality: Personality
    state: State = State.CHASE
