from models import (
    GLOBAL_DOT_LIMITS,
    Ghost,
    GhostPersonality,
    GhostState,
    World,
    dot_limit,
    starve_limit,
)


def preferred(world: World) -> Ghost | None:
    waiting = [g for g in world.ghosts if g.state is GhostState.HOUSE]
    return min(waiting, key=lambda g: g.personality.value, default=None)


def step(world: World, dt: float) -> None:
    world.pacman.starve += dt
    ghost = preferred(world)
    if ghost is None:
        return
    if clyde_waited(world, ghost):
        world.global_dots = None
    if dots_reached(world, ghost):
        ghost.state = GhostState.LEAVING
    elif world.pacman.starve >= starve_limit(world.level):
        ghost.state = GhostState.LEAVING
        world.pacman.starve = 0.0


def clyde_waited(world: World, ghost: Ghost) -> bool:
    return (
        world.global_dots is not None
        and ghost.personality is GhostPersonality.CLYDE
        and world.global_dots >= GLOBAL_DOT_LIMITS[GhostPersonality.CLYDE]
    )


def dots_reached(world: World, ghost: Ghost) -> bool:
    if world.global_dots is None:
        return ghost.dots >= dot_limit(world.level, ghost.personality)
    return world.global_dots >= GLOBAL_DOT_LIMITS[ghost.personality]
