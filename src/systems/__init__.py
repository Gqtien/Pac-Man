from config import Config
from models import World
from .timer import spend
from .pacman import step as pacman_step
from .ghost import step as ghost_step
from .collisions import step as collisions_step
from .house import step as house_step
from .outcome import Outcome


def step(world: World, config: Config, dt: float, keys: set[str]) -> Outcome:
    world.freeze, dt = spend(world.freeze, dt)
    pacman_step(world, config, dt, keys)
    if world.pacman.alive:
        for ghost in world.ghosts:
            ghost_step(ghost, world, config, dt)
        collisions_step(world, config)
        house_step(world, dt)
    return outcome(world, config)


def outcome(world: World, config: Config) -> Outcome:
    if not world.pacman.alive:
        if world.pacman.death < config.anim_speed:
            return Outcome.CONTINUE
        return Outcome.LOST if not world.lives else Outcome.DIED
    if not world.items:
        return Outcome.WON
    return Outcome.CONTINUE


__all__ = ["Outcome", "step"]
