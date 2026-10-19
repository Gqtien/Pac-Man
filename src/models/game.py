from dataclasses import dataclass, field
from .cheat import Cheat
from .direction import Direction
from .entity import Ghost, GhostPersonality, GhostState, Pacman
from .items import Items, init_items
from .map import Map, doors, new_map
from .vec import Vec2


@dataclass
class Level:
    number: int
    map: Map
    items: Items
    pacman: Pacman
    ghosts: list[Ghost]
    timer: float = 0.0
    clock: float = 0.0
    freeze: float = 0.0
    starve: float = 0.0
    multiplier: int = 1
    global_dots: int | None = None


@dataclass
class Game:
    level: Level
    lives: int
    score: int = 0
    cheats: set[Cheat] = field(default_factory=set)


def new_game(lives: int) -> Game:
    return Game(new_level(1, new_map(seed=42)), lives)


def next_level(level: Level) -> Level:
    return new_level(level.number + 1, new_map())


def new_level(number: int, map: Map) -> Level:
    return Level(
        number,
        map,
        init_items(map),
        spawn_pacman(map),
        spawn_ghosts(map),
    )


def respawn(level: Level) -> None:
    dots = {ghost.personality: ghost.dots for ghost in level.ghosts}
    level.pacman = spawn_pacman(level.map)
    level.ghosts = spawn_ghosts(level.map)
    for ghost in level.ghosts:
        ghost.dots = dots[ghost.personality]
    level.starve = 0.0
    level.global_dots = 0


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
            corner=Vec2(width - 2, 1),
            spawn=Vec2(rx + 1, ry),
            state=GhostState.CHASE,
        ),
        Ghost(
            Vec2(lx - 1, ly),
            Direction.NONE,
            GhostPersonality.PINKY,
            corner=Vec2(1, 1),
            spawn=Vec2(lx - 1, ly),
        ),
        Ghost(
            Vec2(rx + 3, ry),
            Direction.NONE,
            GhostPersonality.INKY,
            corner=Vec2(width - 2, height - 2),
            spawn=Vec2(rx + 3, ry),
        ),
        Ghost(
            Vec2(lx - 3, ly),
            Direction.NONE,
            GhostPersonality.CLYDE,
            corner=Vec2(1, height - 2),
            spawn=Vec2(lx - 3, ly),
        ),
    ]
