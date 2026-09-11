from dataclasses import dataclass
from enum import Enum, auto
from models import Vec2, Color


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
    state: State
