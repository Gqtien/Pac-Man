from dataclasses import dataclass
from .pacman import Pacman
from .ghost import Ghost


@dataclass
class World:
    map: list[list[int]]
    pacman: Pacman
    ghosts: list[Ghost]
    score: int = 0
