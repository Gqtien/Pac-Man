from dataclasses import dataclass, replace
from .direction import Direction
from .entity import Ghost, GhostPersonality, Pacman
from .items import Items, init_items
from .map import Map
from .vec import Vec2


@dataclass
class World:
    map: Map
    items: Items
    pacman: Pacman
    ghosts: list[Ghost]
    score: int = 0
    level: int = 1
    freeze: float = 0.0


def new_world(map: Map) -> World:
    return World(map, init_items(map), spawn_pacman(), spawn_ghosts())


def next_level(world: World, map: Map) -> World:
    return replace(new_world(map), score=world.score, level=world.level + 1)


def spawn_pacman() -> Pacman:
    return Pacman(Vec2(1, 1), Direction.NONE)


def spawn_ghosts() -> list[Ghost]:
    return [
        Ghost(Vec2(11, 1), Direction.NONE, GhostPersonality.BLINKY),
        Ghost(Vec2(11, 3), Direction.NONE, GhostPersonality.PINKY),
        Ghost(Vec2(11, 5), Direction.NONE, GhostPersonality.INKY),
        Ghost(Vec2(11, 7), Direction.NONE, GhostPersonality.CLYDE),
    ]
