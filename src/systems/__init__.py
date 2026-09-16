from config import Config
from models import World
from .pacman import step as pacman_step
from .ghost import step as ghost_step
from .collisions import step as collisions_step
from .outcome import Outcome


def step(world: World, config: Config, dt: float, keys: set[str]) -> Outcome:
    pacman_step(world, config, dt, keys)
    for ghost in world.ghosts:
        ghost_step(ghost, world, config, dt)
    collisions_step(world, config)
    return outcome(world)


def outcome(world: World) -> Outcome:
    if not world.pacman:
        return Outcome.LOST
    if not world.items:
        return Outcome.WON
    return Outcome.CONTINUE


__all__ = ["Outcome", "step"]
