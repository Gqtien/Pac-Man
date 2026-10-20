from models import Game, next_level, respawn
from storage import Config
from .cheats import step as cheats_step
from .collisions import step as collisions_step
from .ghost import step as ghost_step
from .house import step as house_step
from .outcome import Outcome
from .pacman import step as pacman_step
from .timer import spend


def step(
    game: Game, config: Config, dt: float, keys: set[int]
) -> Outcome | None:
    level = game.level
    cheats_step(game, config, keys)
    level.freeze, dt = spend(level.freeze, dt)
    level.clock += dt
    pacman_step(level, config, dt, keys)
    if level.pacman.alive:
        level.timer += dt
        for ghost in level.ghosts:
            ghost_step(ghost, game, config, dt)
        collisions_step(game, config)
        house_step(level, dt)
    return advance(game, config)


def advance(game: Game, config: Config) -> Outcome | None:
    level = game.level
    if not level.pacman.alive:
        if level.pacman.death_progress < 1.0 and level.items:
            return None
        if game.lives <= 0:
            return Outcome.LOST
        respawn(level)
    elif level.timer >= config.level_time_limit:
        return Outcome.TIMED_OUT
    elif not level.items:
        if level.number >= config.levels_to_win:
            return Outcome.WON
        game.level = next_level(level)
    return None


__all__ = ["Outcome", "step"]
