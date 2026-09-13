from dataclasses import dataclass
from .vec import Vec2


@dataclass
class Pacman:
    pos: Vec2
    direction: Vec2
    movement_progress: float = 0.0
