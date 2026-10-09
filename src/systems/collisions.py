from storage import Config
from models import Cheat, World, Item, GhostState, Entity, Ghost
from .house import preferred


def step(world: World, config: Config) -> None:
    eat(world)
    collide(world, config)


def eat(world: World) -> None:
    item = world.items.pop(world.pacman.pos, None)
    if item is None:
        return
    world.score += item.value
    world.pacman.stall += item.stall
    if item is Item.PACGUM:
        world.pacman.starve = 0.0
        if world.global_dots is not None:
            world.global_dots += 1
        elif (ghost := preferred(world)) is not None:
            ghost.dots += 1
    if item is Item.SUPER_PACGUM:
        for ghost in world.ghosts:
            if ghost.state in (
                GhostState.CHASE,
                GhostState.SCATTER,
                GhostState.FRIGHTENED,
            ):
                ghost.state = GhostState.FRIGHTENED
                ghost.frightened = 10
                world.multiplier = 1


def collide(world: World, config: Config) -> None:
    for ghost in world.ghosts:
        if not world.pacman.alive:
            break
        if touching(world.pacman, ghost, config.entity_hitbox):
            apply(world, ghost)


def touching(a: Entity, b: Entity, hitbox: float) -> bool:
    (ax, ay), (bx, by) = a.center, b.center
    return abs(ax - bx) < hitbox and abs(ay - by) < hitbox


def apply(world: World, ghost: Ghost) -> None:
    match ghost.state:
        case GhostState.FRIGHTENED:
            ghost.state = GhostState.EATEN
            ghost.bounty = 200 * world.multiplier
            world.score += ghost.bounty
            world.multiplier *= 2
            world.freeze = 1.0
        case GhostState.DEAD | GhostState.EATEN:
            pass
        case GhostState.CHASE | GhostState.SCATTER | GhostState.LEAVING:
            if Cheat.INVINCIBLE in world.cheats:
                return
            world.pacman.alive = False
            world.lives -= 1
            world.freeze += 0.5
