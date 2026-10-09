from models import Map, Vec2, Direction, can_cross, is_wall


def pathfind(
    start: Vec2,
    target: Vec2,
    map: Map,
    restricted_init_dir: Direction = Direction.NONE,
    door_open: bool = False,
) -> list[Vec2]:
    if not is_valid_pos(target, map):
        return []
    to_visit: list[Vec2] = [start]
    visited: set[Vec2] = set()
    previous: dict[Vec2, Vec2] = {}
    while to_visit:
        current = to_visit.pop(0)
        if current == target:
            return build_path(previous, target)
        visited.add(current)
        neighbors: list[Vec2] = []
        if current == start:
            neighbors = get_neighbors(
                current, visited, map, door_open, restricted_init_dir
            )
        else:
            neighbors = get_neighbors(current, visited, map, door_open)
        for cell in neighbors:
            to_visit.append(cell)
            previous[cell] = current
    # no path found
    return []


def is_valid_pos(pos: Vec2, map: Map) -> bool:
    width = len(map[0])
    height = len(map)
    if not (0 <= pos.x < width):
        return False
    if not (0 <= pos.y < height):
        return False
    if is_wall(map[pos.y][pos.x]):
        return False
    return True


def get_neighbors(
    current: Vec2,
    visited: set[Vec2],
    map: Map,
    door_open: bool = False,
    restricted_dir: Direction = Direction.NONE,
) -> list[Vec2]:
    neighbors: list[Vec2] = []
    for direction in (
        Direction.SOUTH,
        Direction.NORTH,
        Direction.EAST,
        Direction.WEST,
    ):
        if direction is restricted_dir:
            continue
        neighbor = current + direction.vec
        if neighbor in visited:
            continue
        if not is_valid_pos(neighbor, map):
            continue
        here, there = map[current.y][current.x], map[neighbor.y][neighbor.x]
        if not can_cross(here, there, door_open):
            continue
        neighbors.append(neighbor)
    return neighbors


def build_path(
    previous: dict[Vec2, Vec2], target: Vec2
) -> list[Vec2]:
    path: list[Vec2] = []
    current: Vec2 | None = target
    while current is not None:
        path.append(current)
        current = previous.get(current)
    path.reverse()
    return path
