from models import Ghost, GhostState, World, speeds


def pacman_factor(world: World) -> float:
    speed = speeds(world.level).pacman
    frightened = any(g.state is GhostState.FRIGHTENED for g in world.ghosts)
    return speed.fright if frightened else speed.default


def ghost_factor(ghost: Ghost, world: World) -> float:
    speed = speeds(world.level).ghost
    if ghost.state is GhostState.FRIGHTENED:
        return speed.fright
    return speed.default
