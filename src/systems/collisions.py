from models import Cheat, Entity, Game, Ghost, GhostState, Item
from storage import Config
from .house import preferred


def step(game: Game, config: Config) -> None:
    eat(game)
    if game.level.items:
        collide(game, config)


def eat(game: Game) -> None:
    level = game.level
    item = level.items.pop(level.pacman.pos, None)
    if item is None:
        return
    game.score += item.value
    level.pacman.stall += item.stall
    if item is Item.PACGUM:
        level.starve = 0.0
        if level.global_dots is not None:
            level.global_dots += 1
        elif (ghost := preferred(level)) is not None:
            ghost.dots += 1
    if item is Item.SUPER_PACGUM:
        for ghost in level.ghosts:
            if ghost.state in (
                GhostState.CHASE,
                GhostState.SCATTER,
                GhostState.FRIGHTENED,
            ):
                ghost.state = GhostState.FRIGHTENED
                ghost.frightened = 10
                level.multiplier = 1


def collide(game: Game, config: Config) -> None:
    level = game.level
    for ghost in level.ghosts:
        if not level.pacman.alive:
            break
        if touching(level.pacman, ghost, config.entity_hitbox):
            apply(game, ghost)


def touching(a: Entity, b: Entity, hitbox: float) -> bool:
    (ax, ay), (bx, by) = a.center, b.center
    return abs(ax - bx) < hitbox and abs(ay - by) < hitbox


def apply(game: Game, ghost: Ghost) -> None:
    level = game.level
    match ghost.state:
        case GhostState.FRIGHTENED:
            ghost.state = GhostState.EATEN
            ghost.bounty = 200 * level.multiplier
            game.score += ghost.bounty
            level.multiplier *= 2
            level.freeze = 1.0
        case GhostState.DEAD | GhostState.EATEN:
            pass
        case GhostState.CHASE | GhostState.SCATTER | GhostState.LEAVING:
            if Cheat.INVINCIBLE in game.cheats:
                return
            level.pacman.alive = False
            game.lives -= 1
