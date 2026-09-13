from models import Direction, World, Ghost, State, Personality, Map
from typing import Callable
from . import movement
from .pathfind import pathfind
from .movement import can_move
import random


def update_blinky(ghost: Ghost, world: World) -> None:
    path = pathfind(ghost.pos, world.pacman.pos, world.map)
    if not path or not path[1:]:
        ghost.direction = Direction.NONE
        return
    next_x, next_y = path[1]
    dx, dy = next_x - ghost.pos.x, next_y - ghost.pos.y
    ghost.direction = Direction((dx, dy))


def update_pinky(ghost: Ghost, world: World) -> None:
    pass


def update_inky(ghost: Ghost, world: World) -> None:
    pass


def update_clyde(ghost: Ghost, world: World) -> None:
    pass


chase_map: dict[Personality, Callable[[Ghost, World], None]] = {
    Personality.BLINKY: update_blinky,
    Personality.PINKY: update_pinky,
    Personality.INKY: update_inky,
    Personality.CLYDE: update_clyde,
}


def update_ghost_frightned(ghost: Ghost, maze: Map) -> None:
    dirs = list(map(Direction, [(0, 1), (1, 0), (0, -1), (-1, 0)]))
    possible_dirs = []
    for dir in dirs:
        if can_move(ghost.pos, dir, maze):
            possible_dirs.append(dir)
    # FIXME: the ghost does sometimes turn around. How ?
    if ghost.direction.opposite in possible_dirs:
        possible_dirs.remove(ghost.direction.opposite)
    ghost.wanted = random.choice(possible_dirs)


def step(ghost: Ghost, world: World, dt: float) -> None:
    movement.move(ghost, world, dt)
    if ghost.dirty:
        # recompute direction
        match ghost.state:
            case State.DEAD:
                pass  # TODO: go back to spawn
            case State.FRIGHTENED:
                update_ghost_frightned(ghost, world.map)
            case State.SCATTER:
                pass  # TODO: go to each personality's corner
            case State.CHASE:
                chase_map[ghost.personality](ghost, world)
