from models import Direction, Entity, Map, Vec2, World


def move(entity: Entity, world: World, dt: float) -> None:
    if not entity.direction.is_still:
        entity.progress += world.config.speed * dt
        if entity.progress < 1.0:
            entity.dirty = False
            return
        entity.progress -= 1.0
        entity.pos.x += entity.direction.dx
        entity.pos.y += entity.direction.dy
        entity.dirty = True

    map = world.map
    if not entity.wanted.is_still and can_move(entity.pos, entity.wanted, map):
        entity.direction = entity.wanted
    elif not can_move(entity.pos, entity.direction, map):
        entity.direction = Direction.NONE


def can_move(pos: Vec2, direction: Direction, map: Map) -> bool:
    x = pos.x + direction.dx
    y = pos.y + direction.dy
    if x < 0 or y < 0:
        return False
    if x >= len(map[0]) or y >= len(map):
        return False
    return not map[y][x]
