from models import (
    GLOBAL_DOT_LIMITS,
    Ghost,
    GhostPersonality,
    GhostState,
    Level,
    dot_limit,
    starve_limit,
)


def preferred(level: Level) -> Ghost | None:
    waiting = [g for g in level.ghosts if g.state is GhostState.HOUSE]
    return min(waiting, key=lambda g: g.personality.value, default=None)


def step(level: Level, dt: float) -> None:
    level.starve += dt
    ghost = preferred(level)
    if ghost is None:
        return
    if clyde_waited(level, ghost):
        level.global_dots = None
    if dots_reached(level, ghost):
        ghost.state = GhostState.LEAVING
    elif level.starve >= starve_limit(level.number):
        ghost.state = GhostState.LEAVING
        level.starve = 0.0


def clyde_waited(level: Level, ghost: Ghost) -> bool:
    return (
        level.global_dots is not None
        and ghost.personality is GhostPersonality.CLYDE
        and level.global_dots >= GLOBAL_DOT_LIMITS[GhostPersonality.CLYDE]
    )


def dots_reached(level: Level, ghost: Ghost) -> bool:
    if level.global_dots is None:
        return ghost.dots >= dot_limit(level.number, ghost.personality)
    return level.global_dots >= GLOBAL_DOT_LIMITS[ghost.personality]
