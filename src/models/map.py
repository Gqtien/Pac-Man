from typing import TypeAlias
from .direction import Direction

Maze: TypeAlias = list[list[int]]
Map: TypeAlias = list[list[int]]

WALLS = {
    Direction.NORTH: 0b0001,
    Direction.EAST: 0b0010,
    Direction.SOUTH: 0b0100,
    Direction.WEST: 0b1000,
}


def has_wall(cell: int, direction: Direction) -> bool:
    return cell & WALLS[direction] != 0


def open_sides(cell: int) -> list[Direction]:
    return [direction for direction in WALLS if not has_wall(cell, direction)]


def from_maze(maze: Maze) -> Map:
    return grid_to_walls(maze_to_grid(maze))


def maze_to_grid(maze: Maze) -> list[list[bool]]:
    height = len(maze)
    if height == 0:
        return []
    width = len(maze[0])

    grid = [[True] * (width * 2 + 1) for _ in range(height * 2 + 1)]

    for y in range(height):
        for x in range(width):
            cell = maze[y][x]
            cx = 2 * x + 1
            cy = 2 * y + 1

            grid[cy][cx] = all(
                (
                    cell & WALLS[Direction.NORTH],
                    cell & WALLS[Direction.SOUTH],
                    cell & WALLS[Direction.WEST],
                    cell & WALLS[Direction.EAST],
                )
            )

            grid[cy - 1][cx] = cell & WALLS[Direction.NORTH] != 0
            grid[cy + 1][cx] = cell & WALLS[Direction.SOUTH] != 0
            grid[cy][cx - 1] = cell & WALLS[Direction.WEST] != 0
            grid[cy][cx + 1] = cell & WALLS[Direction.EAST] != 0

    fill_holes(grid)
    return grid


def fill_holes(grid: list[list[bool]]) -> None:
    height = len(grid)
    if height == 0:
        return
    width = len(grid[0])

    to_fill: list[tuple[int, int]] = []
    for y in range(1, height - 1):
        for x in range(1, width - 1):
            if all(
                (grid[y + dy][x + dx] == False)
                for dx in range(-1, 2)
                for dy in range(-1, 2)
            ):
                to_fill.append((x, y))
    for x, y in to_fill:
        grid[y][x] = True


def grid_to_walls(grid: list[list[bool]]) -> Map:
    height = len(grid)
    if height == 0:
        return []
    width = len(grid[0])
    walls: Map = [[0] * width for _ in range(height)]

    for y in range(height):
        for x in range(width):
            if not grid[y][x]:
                continue
            cell = 0
            if y - 1 >= 0 and grid[y - 1][x]:
                cell |= WALLS[Direction.NORTH]
            if y + 1 < height and grid[y + 1][x]:
                cell |= WALLS[Direction.SOUTH]
            if x - 1 >= 0 and grid[y][x - 1]:
                cell |= WALLS[Direction.WEST]
            if x + 1 < width and grid[y][x + 1]:
                cell |= WALLS[Direction.EAST]
            walls[y][x] = cell if cell else 0x10
    return walls
