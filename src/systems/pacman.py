from config import Config
from models import Direction, Pacman, World
from .movement import move
from .animate import animate
from .speed import pacman_factor
from .timer import spend

KEYMAP: dict[str, Direction] = {
    "Up": Direction.NORTH,
    "Down": Direction.SOUTH,
    "Left": Direction.WEST,
    "Right": Direction.EAST,
}


def step(world: World, config: Config, dt: float, keys: set[str]) -> None:
    if not world.pacman.alive:
        world.pacman.death += dt
        return
    steer(world.pacman, keys)
    world.pacman.stall, dt = spend(world.pacman.stall, dt)
    factor = pacman_factor(world)
    move(world.pacman, world, config.speed * factor, dt)
    animate(world.pacman, config.anim_speed * factor, dt)


def steer(pacman: Pacman, keys: set[str]) -> None:
    for key in keys:
        if key in KEYMAP:
            pacman.wanted = KEYMAP[key]
