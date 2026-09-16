import random
from typing import Callable
from config import Config
from .pathfind import pathfind
from .movement import can_move, move
from .animate import animate
from .speed import ghost_factor
from models import (
    Direction,
    World,
    Ghost,
    GhostState,
    GhostPersonality,
    Map,
    Vec2,
)


def pathfind_to(
        source: Vec2, target: Vec2, map: Map, ghost_dir: Direction
) -> Direction:
    path = pathfind(source, target, map, restricted_init_dir=ghost_dir.opposite)
    if not path or not path[1:]:
        return Direction.NONE
    next_x, next_y = path[1]
    dx, dy = next_x - source.x, next_y - source.y
    return Direction((dx, dy))


def update_blinky(ghost: Ghost, world: World) -> None:
    ghost.direction = pathfind_to(
        ghost.pos, world.pacman.pos, world.map, ghost.direction
    )


def update_pinky(ghost: Ghost, world: World) -> None:
    target: Vec2 = world.pacman.pos + Vec2(*world.pacman.direction.value) * 2
    ghost.direction = pathfind_to(
        ghost.pos, target, world.map, ghost.direction
    )


def update_inky(ghost: Ghost, world: World) -> None:
    blinky: Ghost = next(
        g for g in world.ghosts if g.personality == GhostPersonality.BLINKY
    )
    d: Vec2 = world.pacman.pos + Vec2(*world.pacman.direction.value)
    d -= blinky.pos
    d *= 2
    target = blinky.pos + d
    ghost.direction = pathfind_to(ghost.pos, target, world.map, ghost.direction)


def update_clyde(ghost: Ghost, world: World) -> None:
    ghost.direction = pathfind_to(
        ghost.pos, world.pacman.pos, world.map, ghost.direction
    )
    if (world.pacman.pos - ghost.pos).norm() <= 8:
        ghost.state = GhostState.SCATTER


chase_map: dict[GhostPersonality, Callable[[Ghost, World], None]] = {
    GhostPersonality.BLINKY: update_blinky,
    GhostPersonality.PINKY: update_pinky,
    GhostPersonality.INKY: update_inky,
    GhostPersonality.CLYDE: update_clyde,
}


def update_frightened_dir(ghost: Ghost, maze: Map) -> None:
    dirs = list(map(Direction, [(0, 1), (1, 0), (0, -1), (-1, 0)]))
    possible_dirs = []
    for dir in dirs:
        if can_move(ghost.pos, dir, maze):
            possible_dirs.append(dir)
    if ghost.direction.opposite in possible_dirs:
        possible_dirs.remove(ghost.direction.opposite)
    ghost.direction = random.choice(possible_dirs)


def step(ghost: Ghost, world: World, config: Config, dt: float) -> None:
    factor = ghost_factor(ghost, world)
    move(ghost, world, config.speed * factor, dt)
    animate(ghost, config.anim_speed * factor, dt)

    if ghost.state == GhostState.FRIGHTENED:
        ghost.frightened_timer -= dt
        if ghost.frightened_timer <= 0.0:
            ghost.state = GhostState.CHASE

    if ghost.dirty or ghost.direction is Direction.NONE:
        # recompute direction
        match ghost.state:
            case GhostState.FRIGHTENED:
                update_frightened_dir(ghost, world.map)
            case GhostState.SCATTER | GhostState.DEAD:
                ghost.direction = pathfind_to(
                    ghost.pos, ghost.home, world.map, ghost.direction
                )
                if ghost.pos == ghost.home:
                    ghost.state = GhostState.CHASE
            case GhostState.CHASE:
                chase_map[ghost.personality](ghost, world)
        ghost.dirty = False
