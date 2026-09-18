from dataclasses import dataclass, replace
from .direction import Direction
from .entity import Ghost, GhostPersonality, GhostState, Pacman
from .items import Items, init_items
from .map import Map, doors
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
    y = height - 4
    return Pacman(Vec2(x, y), Direction.NONE)


def spawn_ghosts(map: Map) -> list[Ghost]:
    height = len(map)
    width = len(map[0])
    (lx, ly), (rx, ry) = sorted(doors(map))
    return [
        Ghost(
            Vec2((lx + rx) // 2, ly),
            Direction.NONE,
            GhostPersonality.BLINKY,
            home=Vec2(width - 2, 1),
            spawn=Vec2(rx + 1, ry),
            state=GhostState.CHASE,
        ),
        Ghost(
            Vec2(lx - 1, ly),
            Direction.NONE,
            GhostPersonality.PINKY,
            home=Vec2(1, 1),
            spawn=Vec2(lx - 1, ly),
        ),
        Ghost(
            Vec2(rx + 3, ry),
            Direction.NONE,
            GhostPersonality.INKY,
            home=Vec2(width - 2, height - 2),
            spawn=Vec2(rx + 3, ry),
        ),
        Ghost(
            Vec2(lx - 3, ly),
            Direction.NONE,
            GhostPersonality.CLYDE,
            home=Vec2(1, height - 2),
            spawn=Vec2(lx - 3, ly),
        ),
    ]
