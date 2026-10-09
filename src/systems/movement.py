from models import Direction, Entity, Map, Vec2, World, can_cross


def move(
    entity: Entity, world: World, speed: float, dt: float,
    door_open: bool = False
) -> None:
    if entity.direction.is_still:
        entity.progress = 0.0
    # update direction from wanted
    if entity.just_moved and \
       not entity.wanted.is_still and \
       can_move(entity.pos, entity.wanted, world.map, door_open):
        entity.direction = entity.wanted
    # update progress from direction
    if entity.direction.is_still:
        return
    if not can_move(entity.pos, entity.direction, world.map, door_open):
        entity.direction = Direction.NONE
        return
    entity.progress += speed * dt
    # update pos from progress
    if entity.progress < 1.0:
        entity.just_moved = False
        return
    entity.progress -= 1.0
    entity.pos += entity.direction.vec
    entity.just_moved = True


def can_move(
    pos: Vec2, direction: Direction, map: Map, door_open: bool = False
) -> bool:
    if direction.is_still:
        return True
    to = pos + direction.vec
    if to.x < 0 or to.y < 0:
        return False
    if to.x >= len(map[0]) or to.y >= len(map):
        return False
    return can_cross(map[pos.y][pos.x], map[to.y][to.x], door_open)
