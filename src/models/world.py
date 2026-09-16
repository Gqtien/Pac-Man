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
    return World(map, init_items(map), spawn_pacman(map), spawn_ghosts(map))


def next_level(world: World, map: Map) -> World:
    return replace(new_world(map), score=world.score, level=world.level + 1)


def spawn_pacman(map: Map) -> Pacman:
    height = len(map)
    width = len(map[0])
    x = width // 2
    y = height // 2
    return Pacman(Vec2(x, y), Direction.NONE)


def spawn_ghosts(map: Map) -> list[Ghost]:
    height = len(map)
    width = len(map[0])
    return [
        Ghost(Vec2(width - 2, 1), Direction.NONE, GhostPersonality.BLINKY, home=Vec2(width - 2, 1)),
        Ghost(Vec2(width - 2, height - 2), Direction.NONE, GhostPersonality.INKY, home=Vec2(width - 2, height - 2)),
        Ghost(Vec2(1, 1), Direction.NONE, GhostPersonality.PINKY, home=Vec2(1, 1)),
        Ghost(Vec2(1, height - 2), Direction.NONE, GhostPersonality.CLYDE, home=Vec2(1, height - 2)),
    ]
