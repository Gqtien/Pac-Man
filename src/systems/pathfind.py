from models import Map, Vec2, Direction


def to_tuple(a: Vec2) -> tuple[int, int]:
    """Vector2 to tuple."""
    return (int(a.x), int(a.y))


def pathfind(
        start: Vec2, target: Vec2, map: Map,
        restricted_init_dir: Direction = Direction.NONE
) -> list[tuple[int, int]]:
    """Breadth first search in a 2D grid.

    Return an empty list if there is no path.
    """

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
                current, visited, map, restricted_init_dir
            )
        else:
            neighbors = get_neighbors(current, visited, map)
        for cell in neighbors:
            to_visit.append(cell)
            previous[cell] = current
    # no path found
    return []


def is_valid_pos(pos: tuple[int, int], maze: list[list[int]]) -> bool:
    """Is pos inbound and not a wall."""
    width = len(maze[0])
    height = len(maze)
    x, y = pos
    if not (0 <= x < width):
        return False
    if not (0 <= y < height):
        return False
    if maze[y][x]:
        return False
    return True


def get_neighbors(
        current: tuple[int, int],
        visited: set[tuple[int, int]],
        maze: list[list[int]],
        restricted_dir: Direction = Direction.NONE
) -> list[tuple[int, int]]:
    """Get surounding cells that are not visited nor a wall."""
    x, y = current
    neighbors: list[tuple[int, int]] = []
    directions = [
        (0, 1), (0, -1), (1, 0), (-1, 0)
    ]
    if restricted_dir.value in directions:
        directions.remove(restricted_dir.value)
    for dx, dy in directions:
        neighbor = (x + dx, y + dy)
        if neighbor in visited:
            continue
        if not is_valid_pos(neighbor, maze):
            continue
        neighbors.append(neighbor)
    return neighbors


def build_path(
        previous: dict[tuple[int, int], tuple[int, int]],
        target: tuple[int, int]
) -> list[tuple[int, int]]:
    """Reconstruct path from previous dict."""
    path: list[tuple[int, int]] = []
    current: tuple[int, int] | None = target
    while current:
        path.append(current)
        current = previous.get(current, None)
    path.reverse()
    return path
