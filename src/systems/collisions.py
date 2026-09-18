from config import Config
from models import World, Item, GhostState, Entity, Ghost
from .house import preferred


def step(world: World, config: Config) -> None:
    eat(world)
    collide(world, config)


def eat(world: World) -> None:
    pos = world.pacman.pos
    item = world.items.pop((pos.x, pos.y), None)
    if item is None:
        return
    world.score += item.value
    world.pacman.stall += item.stall
    if item is Item.PACGUM:
        world.pacman.starve = 0.0
        if (ghost := preferred(world)) is not None:
            ghost.dots += 1
    if item is Item.SUPER_PACGUM:
        for ghost in world.ghosts:
            if ghost.state in (
                GhostState.CHASE,
                GhostState.SCATTER,
                GhostState.FRIGHTENED,
            ):
                ghost.state = GhostState.FRIGHTENED
                ghost.frightened_timer = 10
                world.multiplier = 1


def collide(world: World, config: Config) -> None:
    for ghost in world.ghosts:
        if touching(world.pacman, ghost, config.entity_hitbox):
            apply(world, ghost)


def touching(a: Entity, b: Entity, hitbox: float) -> bool:
    (ax, ay), (bx, by) = a.center, b.center
    return abs(ax - bx) < hitbox and abs(ay - by) < hitbox


def apply(world: World, ghost: Ghost) -> None:
    match ghost.state:
        case GhostState.FRIGHTENED:
            ghost.state = GhostState.EATEN
            ghost.value = 200 * world.multiplier
            world.score += ghost.value
            world.multiplier *= 2
            world.freeze = 1.0
        case GhostState.DEAD | GhostState.EATEN:
            pass
        case GhostState.CHASE | GhostState.SCATTER | GhostState.LEAVING:
            if world.pacman.is_invisible:
                return
            world.pacman.alive = False
            world.lives -= 1
            world.freeze += 0.5
