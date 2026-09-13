from models import World
from . import pacman
from .ghost import step as ghost_step
from .outcome import Outcome


def step(world: World, dt: float, keys: set[str]) -> Outcome:
    pacman.step(world, dt, keys)
    for ghost in world.ghosts:
        ghost_step(ghost, world, dt)

    return outcome(world)


def outcome(world: World) -> Outcome:
    if not world.pacman:
        return Outcome.LOST
    # if not pacgums return Outcome.WON
    return Outcome.CONTINUE


__all__ = ["Outcome", "step"]
