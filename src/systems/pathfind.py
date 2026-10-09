from models import Map, Vec2, Direction, can_cross, is_wall


def to_tuple(a: Vec2) -> tuple[int, int]:
    return (int(a.x), int(a.y))


def pathfind(
    start: Vec2,
    target: Vec2,
    map: Map,
    restricted_init_dir: Direction = Direction.NONE,
    door_open: bool = False,
) -> list[tuple[int, int]]:
    goal = to_tuple(target)
    if not is_valid_pos(goal, map):
        return []
    to_visit: list[tuple[int, int]] = [to_tuple(start)]
    visited: set[tuple[int, int]] = set()
    previous: dict[tuple[int, int], tuple[int, int]] = dict()
    while to_visit:
        current = to_visit.pop(0)
        if current == goal:
            return build_path(previous, goal)
        visited.add(current)
        neighbors: list[tuple[int, int]] = []
        if current == to_tuple(start):
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


def is_valid_pos(pos: tuple[int, int], map: Map) -> bool:
    width = len(map[0])
    height = len(map)
    x, y = pos
    if not (0 <= x < width):
        return False
    if not (0 <= y < height):
        return False
    if is_wall(map[y][x]):
        return False
    return True


def get_neighbors(
    current: tuple[int, int],
    visited: set[tuple[int, int]],
    map: Map,
    door_open: bool = False,
    restricted_dir: Direction = Direction.NONE,
) -> list[tuple[int, int]]:
    x, y = current
    neighbors: list[tuple[int, int]] = []
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    if restricted_dir.value in directions:
        directions.remove(restricted_dir.value)
    for dx, dy in directions:
        neighbor = (x + dx, y + dy)
        if neighbor in visited:
            continue
        if not is_valid_pos(neighbor, map):
            continue
        if not can_cross(map[y][x], map[y + dy][x + dx], door_open):
            continue
        neighbors.append(neighbor)
    return neighbors


def build_path(
    previous: dict[tuple[int, int], tuple[int, int]], target: tuple[int, int]
) -> list[tuple[int, int]]:
    path: list[tuple[int, int]] = []
    current: tuple[int, int] | None = target
    while current:
        path.append(current)
        current = previous.get(current, None)
    path.reverse()
    return path
