from dataclasses import dataclass, field
from enum import Enum, auto
from .direction import Direction
from .colors import Color
from .vec import Vec2


class Personality(Enum):
    BLINKY = Color.BLINKY
    PINKY = Color.PINKY
    INKY = Color.INKY
    CLYDE = Color.CLYDE


class State(Enum):
    CHASE = auto()
    SCATTER = auto()
    DEAD = auto()
    FRIGHTENED = auto()


@dataclass
class Entity:
    pos: Vec2
    direction: Direction
    wanted: Direction = field(default=Direction.NONE, kw_only=True)
    progress: float = field(default=0.0, kw_only=True)


@dataclass
class Pacman(Entity): ...


@dataclass
class Ghost(Entity):
    personality: Personality
    state: State = State.CHASE

    @property
    def color(self) -> str:
        return self.personality.value
