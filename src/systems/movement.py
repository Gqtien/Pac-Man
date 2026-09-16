from models import Direction, Entity, Map, Vec2, World


def move(entity: Entity, world: World, speed: float, dt: float) -> None:
    # update direction from wanted
    if entity.just_moved and \
       not entity.wanted.is_still and \
       can_move(entity.pos, entity.wanted, world.map):
        entity.direction = entity.wanted
    # update progress from direction
    if entity.direction.is_still:
        return
    if not can_move(entity.pos, entity.direction, world.map):
        entity.direction = Direction.NONE
        return
    entity.progress += speed * dt
    # update pos from progress
    if entity.progress < 1.0:
        entity.just_moved = False
        return
    entity.progress -= 1.0
    entity.pos.x += entity.direction.dx
    entity.pos.y += entity.direction.dy
    entity.just_moved = True


def can_move(pos: Vec2, direction: Direction, map: Map) -> bool:
    if direction.is_still:
        return True
    x = pos.x + direction.dx
    y = pos.y + direction.dy
    if x < 0 or y < 0:
        return False
    if x >= len(map[0]) or y >= len(map):
        return False
    return not map[y][x]
