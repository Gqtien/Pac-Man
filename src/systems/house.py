from models import World, Ghost, GhostState, dot_limit, starve_limit


def preferred(world: World) -> Ghost | None:
    waiting = [g for g in world.ghosts if g.state is GhostState.HOUSE]
    return min(waiting, key=lambda g: g.personality.value, default=None)


def step(world: World, dt: float) -> None:
    world.pacman.starve += dt
    ghost = preferred(world)
    if ghost is None:
        return
    if ghost.dots >= dot_limit(world.level, ghost.personality):
        ghost.state = GhostState.LEAVING
    elif world.pacman.starve >= starve_limit(world.level):
        ghost.state = GhostState.LEAVING
        world.pacman.starve = 0.0
