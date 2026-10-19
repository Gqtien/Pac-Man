from storage import Config
from models import Direction, Level, Pacman, Keys
from .movement import move
from .speed import pacman_factor
from .timer import spend

KEYMAP: dict[int, Direction] = {
    Keys.Up: Direction.NORTH,
    Keys.Down: Direction.SOUTH,
    Keys.Left: Direction.WEST,
    Keys.Right: Direction.EAST,
}


def step(level: Level, config: Config, dt: float, keys: set[int]) -> None:
    if not level.pacman.alive:
        level.pacman.death += dt
        return
    steer(level.pacman, keys)
    level.pacman.stall, dt = spend(level.pacman.stall, dt)
    factor = pacman_factor(level)
    move(level.pacman, level.map, config.speed * factor, dt)
    if not level.pacman.direction.is_still:
        level.pacman.facing = level.pacman.direction


def steer(pacman: Pacman, keys: set[int]) -> None:
    for key in keys:
        if key in KEYMAP:
            pacman.wanted = KEYMAP[key]
