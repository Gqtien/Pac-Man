from config import Config
from models import World
from .pacman import step as pacman_step
from .ghost import step as ghost_step
from .outcome import Outcome


def step(world: World, config: Config, dt: float, keys: set[str]) -> Outcome:
    pacman_step(world, config, dt, keys)
    for ghost in world.ghosts:
        ghost_step(ghost, world, config, dt)
    return outcome(world)


def outcome(world: World) -> Outcome:
    if not world.pacman:
        return Outcome.LOST
    # if not pacgums return Outcome.WON
    return Outcome.CONTINUE


__all__ = ["Outcome", "step"]
