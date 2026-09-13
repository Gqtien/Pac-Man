from dataclasses import dataclass
from enum import Enum, auto
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
class Ghost:
    pos: Vec2
    direction: Vec2
    personality: Personality
    movement_progress: float = 0.0
    state: State = State.CHASE
