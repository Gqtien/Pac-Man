from typing import TypeAlias
from .direction import Direction
from .vec import Vec2
from mazegenerator import MazeGenerator

Maze: TypeAlias = list[list[int]]
Map: TypeAlias = list[list[int]]

WALLS = {
    Direction.NORTH: 0b0001,
    Direction.EAST: 0b0010,
    Direction.SOUTH: 0b0100,
    Direction.WEST: 0b1000,
}


def new_map() -> Map:
    return from_maze(MazeGenerator().maze)


def has_wall(cell: int, direction: Direction) -> bool:
    return cell & WALLS[direction] != 0


def open_sides(cell: int) -> list[Direction]:
    return [direction for direction in WALLS if not has_wall(cell, direction)]


def is_solid(cell: int) -> bool:
    return cell != 0


def is_house(cell: int) -> bool:
    return cell in (-1, -2, -3)


def is_door(cell: int) -> bool:
    return cell == -2


def is_wall(cell: int) -> bool:
    return cell > 0 or cell == -1


def can_cross(src: int, dst: int, door_open: bool = False) -> bool:
    if is_wall(dst):
        return False
    if is_door(src) or is_door(dst):
        return door_open
    return is_house(src) == is_house(dst)


def doors(map: Map) -> list[Vec2]:
    return [
        Vec2(x, y)
        for y, row in enumerate(map)
        for x, cell in enumerate(row)
        if is_door(cell)
    ]


def from_maze(maze: Maze) -> Map:
    enclosed = enclosed_cells(maze)
    house = house_cells(enclosed)
    inner = inner_cells(house)
    doors = door_cells(enclosed)

    grid = maze_to_grid(maze)
    for cell in house:
        grid[cell.y][cell.x] = False
    map = grid_to_walls(grid)
    for cell in house:
        map[cell.y][cell.x] = -1
    for cell in inner:
        map[cell.y][cell.x] = -3
    for cell in doors:
        map[cell.y][cell.x] = -2
    return map


def enclosed_cells(maze: Maze) -> set[Vec2]:
    return {
        Vec2(x, y)
        for y, line in enumerate(maze)
        for x, cell in enumerate(line)
        if all(has_wall(cell, direction) for direction in WALLS)
    }


def grid_center(cell: Vec2) -> Vec2:
    return cell * 2 + Vec2(1, 1)


def house_cells(enclosed: set[Vec2]) -> set[Vec2]:
    house: set[Vec2] = set()
    for cell in enclosed:
        center = grid_center(cell)
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                house.add(center + Vec2(dx, dy))
    return house


def inner_cells(house: set[Vec2]) -> set[Vec2]:
    return {
        cell
        for cell in house
        if all(
            cell + Vec2(dx, dy) in house
            for dx in (-1, 0, 1)
            for dy in (-1, 0, 1)
        )
    }


def door_cells(enclosed: set[Vec2]) -> set[Vec2]:
    xs = {cell.x for cell in enclosed}
    ys = {cell.y for cell in enclosed}
    middle = Vec2((min(xs) + max(xs)) // 2, (min(ys) + max(ys)) // 2)
    center = grid_center(middle)
    return {center - Vec2(1, 0), center + Vec2(1, 0)}


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

    to_fill: list[Vec2] = []
    for y in range(1, height - 1):
        for x in range(1, width - 1):
            if all(
                (grid[y + dy][x + dx] is False)
                for dx in range(-1, 2)
                for dy in range(-1, 2)
            ):
                to_fill.append(Vec2(x, y))
    for cell in to_fill:
        grid[cell.y][cell.x] = True


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
