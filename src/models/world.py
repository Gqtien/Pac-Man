from dataclasses import dataclass
from .entity import Pacman, Ghost
from .map import Map


@dataclass
class World:
    map: Map
    pacman: Pacman
    ghosts: list[Ghost]
    score: int = 0
