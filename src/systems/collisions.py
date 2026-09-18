from models import World, Item, GhostState, Entity, Ghost
from .house import preferred


def step(world: World) -> None:
    eat(world)
    collide(world)


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
                ghost.frightened_timer = 10  # TODO: config


def collide(world: World) -> None:
    for ghost in world.ghosts:
        if touching(world.pacman, ghost):
            apply(world, ghost)


def touching(a: Entity, b: Entity) -> bool:
    (ax, ay), (bx, by) = a.center, b.center
    return abs(ax - bx) < 1 and abs(ay - by) < 1


def apply(world: World, ghost: Ghost) -> None:
    match ghost.state:
        case GhostState.FRIGHTENED:
            ghost.state = GhostState.DEAD
            world.score += 200
            world.freeze = 1.0
        case GhostState.DEAD:
            pass
        case GhostState.CHASE | GhostState.SCATTER | GhostState.LEAVING:
            world.pacman.alive = False
            world.lives -= 1
