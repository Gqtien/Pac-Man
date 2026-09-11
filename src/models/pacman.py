from dataclasses import dataclass
from models import Vec2


@dataclass
class Pacman:
    pos: Vec2
    direction: Vec2
