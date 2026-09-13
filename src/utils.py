WALL_NORTH = 0b0001
WALL_EAST = 0b0010
WALL_SOUTH = 0b0100
WALL_WEST = 0b1000


def maze_to_grid(maze: list[list[int]]) -> list[list[bool]]:
    height = len(maze)
    if height == 0:
        return []
    width = len(maze[0])

    gw = width * 2 + 1
    gh = height * 2 + 1

    # start full of walls
    grid: list[list[bool]] = [[True] * gw for _ in range(gh)]

    for y in range(height):
        for x in range(width):
            cell = maze[y][x]

            cx = 2 * x + 1
            cy = 2 * y + 1

            # cell center is always a path
            grid[cy][cx] = all((
                cell & WALL_NORTH,
                cell & WALL_SOUTH,
                cell & WALL_WEST,
                cell & WALL_EAST
            ))

            # open passages according to missing walls
            grid[cy - 1][cx] = cell & WALL_NORTH != 0
            grid[cy + 1][cx] = cell & WALL_SOUTH != 0
            grid[cy][cx - 1] = cell & WALL_WEST != 0
            grid[cy][cx + 1] = cell & WALL_EAST != 0

    return grid


def grid_to_walls(grid: list[list[bool]]) -> list[list[int]]:
    """Store adjacent wall info in int for each cell."""
    height = len(grid)
    if height == 0:
        return []
    width = len(grid[0])
    walls: list[list[int]] = [[0] * width for _ in range(height)]

    for y in range(height):
        for x in range(width):
            if not grid[y][x]:
                continue
            cell = 0
            if y - 1 >= 0 and grid[y - 1][x]:
                cell |= WALL_NORTH
            if y + 1 < height and grid[y + 1][x]:
                cell |= WALL_SOUTH
            if x - 1 >= 0 and grid[y][x - 1]:
                cell |= WALL_WEST
            if x + 1 < width and grid[y][x + 1]:
                cell |= WALL_EAST
            walls[y][x] = cell
    return walls
