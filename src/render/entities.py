from assets import Animation, Sprites
from models import Entity, Ghost, GhostState, Pacman, World
from .grid import Grid


def draw_entities(grid: Grid, world: World, sprites: Sprites) -> None:
    pacman = world.pacman
    if pacman.alive or world.freeze > 0:
        draw_entity(grid, pacman, sprites.pacman[pacman.direction])
        for ghost in world.ghosts:
            draw_entity(grid, ghost, ghost_animation(ghost, sprites))
    else:
        draw_death(grid, pacman, sprites.death)


def draw_entity(grid: Grid, entity: Entity, animation: Animation) -> None:
    frame = animation[int(entity.anim_progress) % len(animation)]
    grid.put(frame, *entity.center)


def draw_death(grid: Grid, pacman: Pacman, frames: Animation) -> None:
    index = int(pacman.death_progress * len(frames))
    grid.put(frames[min(index, len(frames) - 1)], *pacman.center)


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
            return [sprites.ghost_score[ghost.value]]
        case GhostState.FRIGHTENED:
            if (
                ghost.frightened_timer < 3
                and int(ghost.frightened_timer * 4) % 2 == 0
            ):
                return sprites.flashing
            return sprites.frightened
