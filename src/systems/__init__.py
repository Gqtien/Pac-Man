from storage import Config
from models import World
from .timer import spend
from .cheats import step as cheats_step
from .pacman import step as pacman_step
from .ghost import step as ghost_step
from .collisions import step as collisions_step
from .house import step as house_step
from .outcome import Outcome


def step(world: World, config: Config, dt: float, keys: set[int]) -> Outcome:
    cheats_step(world, config, keys)
    world.freeze, dt = spend(world.freeze, dt)
    world.clock += dt
    pacman_step(world, config, dt, keys)
    if world.pacman.alive:
        world.timer += dt
        for ghost in world.ghosts:
            ghost_step(ghost, world, config, dt)
        collisions_step(world, config)
        house_step(world, dt)
    return outcome(world, config)


def outcome(world: World, config: Config) -> Outcome:
    if not world.pacman.alive:
        if world.pacman.death_progress < 1.0 and world.items:
            return Outcome.CONTINUE
        return Outcome.LOST if world.lives <= 0 else Outcome.DIED
    if world.timer >= config.level_time_limit:
        return Outcome.TIMED_OUT
    if not world.items:
        return Outcome.WON
    return Outcome.CONTINUE


__all__ = ["Outcome", "step"]
