from dataclasses import dataclass
from .items import Items
from .entity import Pacman, Ghost
from .map import Map


@dataclass
class World:
    map: Map
    items: Items
    pacman: Pacman
    ghosts: list[Ghost]
    score: int = 0
    level: int = 1
