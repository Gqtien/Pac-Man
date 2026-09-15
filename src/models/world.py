from dataclasses import dataclass, field
from config import Config
from .entity import Pacman, Ghost
from .map import Map


@dataclass
class World:
    map: Map
    pacman: Pacman
    ghosts: list[Ghost]
    config: Config = field(default_factory=Config)
    score: int = 0
