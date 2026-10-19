from assets import Animation, Sprites
from models import Ghost, GhostState, Pacman, World
from .grid import Grid


def draw_entities(grid: Grid, world: World, sprites: Sprites) -> None:
    pacman = world.pacman
    if pacman.alive or pacman.death < 0.5:
        for ghost in world.ghosts:
            draw_ghost(grid, ghost, sprites, world.clock)
    if pacman.alive:
        if all(ghost.state is not GhostState.EATEN for ghost in world.ghosts):
            draw_pacman(grid, pacman, sprites)
    elif pacman.death < 1:
        draw_pacman(grid, pacman, sprites)
    else:
        draw_death(grid, pacman, sprites.death)


def draw_pacman(grid: Grid, pacman: Pacman, sprites: Sprites) -> None:
    frames = sprites.pacman[pacman.facing]
    tiles = (pacman.pos.x + pacman.pos.y) % 2 + pacman.progress
    frame = frames[int(tiles * len(frames) / 2) % len(frames)]
    grid.put(frame, *pacman.center)


def draw_ghost(
    grid: Grid, ghost: Ghost, sprites: Sprites, clock: float
) -> None:
    frames = ghost_animation(ghost, sprites)
    grid.put(frames[int(clock * 60 / 8) % len(frames)], *ghost.center)


def draw_death(grid: Grid, pacman: Pacman, frames: Animation) -> None:
    *wilt, burst = frames
    t = pacman.death - 1
    if t < 1:
        grid.put(wilt[int(t * len(wilt))], *pacman.center)
    elif t < 1.25:
        grid.put(burst, *pacman.center)


def ghost_animation(ghost: Ghost, sprites: Sprites) -> Animation:
    match ghost.state:
        case (
            GhostState.CHASE
            | GhostState.SCATTER
            | GhostState.HOUSE
            | GhostState.LEAVING
        ):
            return sprites.ghost[ghost.personality][ghost.direction]
        case GhostState.DEAD:
            return [sprites.eyes[ghost.direction]]
        case GhostState.EATEN:
            return [sprites.ghost_score[ghost.bounty]]
        case GhostState.FRIGHTENED:
            slot = int(ghost.frightened * 60 / 14)
            if slot < 10 and slot % 2 == 0:
                return sprites.flashing
            return sprites.frightened
