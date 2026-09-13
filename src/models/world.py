from dataclasses import dataclass
from .entity import Pacman, Ghost


@dataclass
class World:
    map: list[list[int]]
    pacman: Pacman
    ghosts: list[Ghost]
    score: int = 0
