from models import Cheat, Game, Ghost, GhostState, Level, speeds


def pacman_factor(level: Level) -> float:
    speed = speeds(level.number).pacman
    frightened = any(g.state is GhostState.FRIGHTENED for g in level.ghosts)
    return speed.fright if frightened else speed.default


def ghost_factor(ghost: Ghost, game: Game) -> float:
    if Cheat.FREEZE_GHOSTS in game.cheats:
        return 0.0
    speed = speeds(game.level.number).ghost
    if ghost.state is GhostState.FRIGHTENED:
        return speed.fright
    return speed.default
