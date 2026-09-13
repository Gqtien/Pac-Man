from dataclasses import dataclass, field
from typing import TypeAlias
from config import Config
from .entity import Pacman, Ghost

Map: TypeAlias = list[list[int]]


@dataclass
class World:
    map: Map
    pacman: Pacman
    ghosts: list[Ghost]
    config: Config = field(default_factory=Config)
    score: int = 0
