from dataclasses import dataclass
from models import Pacman, Ghost


@dataclass
class World:
    map: list[list[int]]
    pacman: Pacman
    ghosts: list[Ghost]
    score: int
