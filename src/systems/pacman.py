from config import Config
from models import Direction, Pacman, World
from . import movement
from .animate import animate

KEYMAP: dict[str, Direction] = {
    "Up": Direction.NORTH,
    "Down": Direction.SOUTH,
    "Left": Direction.WEST,
    "Right": Direction.EAST,
}


def step(world: World, config: Config, dt: float, keys: set[str]) -> None:
    steer(world.pacman, keys)
    movement.move(world.pacman, world, config, dt)
    animate(world.pacman, world, config, dt)


def steer(pacman: Pacman, keys: set[str]) -> None:
    for key in keys:
        if key in KEYMAP:
            pacman.wanted = KEYMAP[key]
