from dataclasses import dataclass
from .entity import Pacman, Ghost
from typing import TypeAlias

Map: TypeAlias = list[list[int]]

@dataclass
class World:
    map: Map
    pacman: Pacman
    ghosts: list[Ghost]
    score: int = 0
