import random
from typing import Callable
from storage import Config
from .pathfind import pathfind
from .movement import can_move, move
from .speed import ghost_factor
from models import (
    Direction,
    Game,
    Level,
    Ghost,
    GhostState,
    GhostPersonality,
    Map,
    Vec2,
    is_solid,
)


def pathfind_to(
    source: Vec2,
    target: Vec2,
    map: Map,
    ghost_dir: Direction,
    door_open: bool = False,
) -> Direction:
    path = pathfind(
        source,
        target,
        map,
        restricted_init_dir=ghost_dir.opposite,
        door_open=door_open,
    )
    if not path or not path[1:]:
        return Direction.NONE
    step = path[1] - source
    return Direction((step.x, step.y))


def update_blinky(ghost: Ghost, level: Level) -> None:
    ghost.direction = pathfind_to(
        ghost.pos, level.pacman.pos, level.map, ghost.direction
    )


def update_pinky(ghost: Ghost, level: Level) -> None:
    target = level.pacman.pos + level.pacman.direction.vec * 2
    ghost.direction = pathfind_to(
        ghost.pos, target, level.map, ghost.direction
    )


def update_inky(ghost: Ghost, level: Level) -> None:
    blinky: Ghost = next(
        g for g in level.ghosts if g.personality is GhostPersonality.BLINKY
    )
    ahead = level.pacman.pos + level.pacman.direction.vec
    target = blinky.pos + (ahead - blinky.pos) * 2
    ghost.direction = pathfind_to(
        ghost.pos, target, level.map, ghost.direction
    )


def update_clyde(ghost: Ghost, level: Level) -> None:
    ghost.direction = pathfind_to(
        ghost.pos, level.pacman.pos, level.map, ghost.direction
    )
    if (level.pacman.pos - ghost.pos).norm() <= 8:
        ghost.state = GhostState.SCATTER


CHASE_MAP: dict[GhostPersonality, Callable[[Ghost, Level], None]] = {
    GhostPersonality.BLINKY: update_blinky,
    GhostPersonality.PINKY: update_pinky,
    GhostPersonality.INKY: update_inky,
    GhostPersonality.CLYDE: update_clyde,
}


def update_frightened_dir(ghost: Ghost, map: Map) -> None:
    possible_dirs = []
    for dir in [dir for dir in Direction if not dir.is_still]:
        if can_move(ghost.pos, dir, map):
            possible_dirs.append(dir)
    if ghost.direction.opposite in possible_dirs and len(possible_dirs) > 1:
        possible_dirs.remove(ghost.direction.opposite)
    ghost.direction = random.choice(possible_dirs)


def idle(ghost: Ghost, map: Map) -> None:
    options = [
        direction
        for direction in [d for d in Direction if not d.is_still]
        if direction is not ghost.direction.opposite
        and can_move(ghost.pos, direction, map)
    ]
    ghost.direction = options[0] if options else ghost.direction.opposite


def step(ghost: Ghost, game: Game, config: Config, dt: float) -> None:
    level = game.level
    factor = ghost_factor(ghost, game)
    door_open = ghost.state in (GhostState.LEAVING, GhostState.DEAD)
    move(ghost, level.map, config.speed * factor, dt, door_open)

    if ghost.state is GhostState.FRIGHTENED:
        ghost.frightened -= dt
        if ghost.frightened <= 0.0:
            ghost.state = GhostState.CHASE
    if ghost.state is GhostState.EATEN and not level.freeze:
        ghost.state = GhostState.DEAD

    if ghost.just_moved or ghost.direction is Direction.NONE:
        # recompute direction
        match ghost.state:
            case GhostState.HOUSE:
                idle(ghost, level.map)
            case GhostState.LEAVING:
                ghost.direction = pathfind_to(
                    ghost.pos,
                    ghost.corner,
                    level.map,
                    ghost.direction,
                    door_open=True,
                )
                if not is_solid(level.map[ghost.pos.y][ghost.pos.x]):
                    ghost.state = GhostState.CHASE
            case GhostState.DEAD:
                ghost.direction = pathfind_to(
                    ghost.pos,
                    ghost.spawn,
                    level.map,
                    ghost.direction,
                    door_open=True,
                )
                if ghost.pos == ghost.spawn:
                    ghost.state = GhostState.HOUSE
            case GhostState.EATEN:
                pass
            case GhostState.FRIGHTENED:
                update_frightened_dir(ghost, level.map)
            case GhostState.SCATTER:
                ghost.direction = pathfind_to(
                    ghost.pos, ghost.corner, level.map, ghost.direction
                )
                if ghost.pos == ghost.corner:
                    ghost.state = GhostState.CHASE
            case GhostState.CHASE:
                CHASE_MAP[ghost.personality](ghost, level)
        ghost.just_moved = False
