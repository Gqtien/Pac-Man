from storage import Config
from models import Direction, Pacman, World, Keys
from .movement import move
from .animate import animate
from .speed import pacman_factor
from .timer import spend

KEYMAP: dict[int, Direction] = {
    Keys.Up: Direction.NORTH,
    Keys.Down: Direction.SOUTH,
    Keys.Left: Direction.WEST,
    Keys.Right: Direction.EAST,
}


def step(world: World, config: Config, dt: float, keys: set[int]) -> None:
    if config.cheat_invincible_key in keys:
        world.pacman.invincible = not world.pacman.invincible
    if not world.pacman.alive:
        world.pacman.death += dt
        return
    steer(world.pacman, keys)
    world.pacman.stall, dt = spend(world.pacman.stall, dt)
    factor = pacman_factor(world)
    move(world.pacman, world, config.speed * factor, dt)
    animate(world.pacman, config.anim_speed * factor, dt)


def steer(pacman: Pacman, keys: set[int]) -> None:
    for key in keys:
        if key in KEYMAP:
            pacman.wanted = KEYMAP[key]
