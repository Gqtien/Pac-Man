from models import World, Item, GhostState, Entity, Ghost


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
    if item is Item.SUPER_PACGUM:
        for ghost in world.ghosts:
            if ghost.state is not GhostState.DEAD:
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
        case GhostState.CHASE | GhostState.SCATTER:
            world.pacman.alive = False
