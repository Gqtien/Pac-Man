from typing import Callable, TypeAlias
from assets import Wall, Walls
from models import Direction, Map, is_door, is_house, is_solid
from .grid import Grid

Frame: TypeAlias = dict[
    tuple[Direction, Direction],
    tuple[Wall, Wall, Wall, Wall],
]
Quarter: TypeAlias = tuple[Wall, Direction, Direction]


def frame(corner: str, edge: str, inner: str) -> Frame:
    tiles = {}
    for v in (Direction.NORTH, Direction.SOUTH):
        for h in (Direction.WEST, Direction.EAST):
            quarter = v.name[0] + h.name[0]
            tiles[v, h] = (
                Wall[f"{corner}_{quarter}"],
                Wall[f"{edge}_{v.name[0]}"],
                Wall[f"{edge}_{h.name[0]}"],
                Wall[f"{inner}_{quarter}"],
            )
    return tiles


FRAME = frame("CORNER", "EDGE", "INNER")
HOUSE_FRAME = frame("HOUSE", "EDGE", "HOUSE_INNER")
RIM = frame("RIM", "RIM", "RIM_INNER")

DOOR = {
    Direction.EAST: (Wall.DOOR_E_TOP, Wall.DOOR_E_BOTTOM),
    Direction.WEST: (Wall.DOOR_W_TOP, Wall.DOOR_W_BOTTOM),
}


def draw_maze(grid: Grid, map: Map, walls: Walls) -> None:
    for y, line in enumerate(map):
        for x, cell in enumerate(line):
            if not is_solid(cell):
                continue
            for wall, v, h in quarters(map, x, y):
                grid.put(
                    walls[wall],
                    x + (0.5 if h is Direction.EAST else 0),
                    y + (0.5 if v is Direction.SOUTH else 0),
                )


def quarters(map: Map, x: int, y: int) -> list[Quarter]:
    cell = map[y][x]
    if is_door(cell):
        side = Direction.EAST
        if is_solid(cell_at(map, x + 1, y)):
            side = Direction.WEST
        top, bottom = DOOR[side]
        return [(top, Direction.NORTH, side), (bottom, Direction.SOUTH, side)]
    if is_house(cell):
        return (
            frame_quarters(map, x, y, HOUSE_FRAME, is_solid)
            + frame_quarters(map, x, y, RIM, is_house)
        )
    return frame_quarters(map, x, y, FRAME, is_solid)


def frame_quarters(
    map: Map, x: int, y: int, frame: Frame, joined: Callable[[int], bool]
) -> list[Quarter]:
    tiles: list[Quarter] = []
    for (v, h), (corner, edge_v, edge_h, inner) in frame.items():
        side_v = joined(cell_at(map, x, y + v.dy))
        side_h = joined(cell_at(map, x + h.dx, y))
        diagonal = joined(cell_at(map, x + h.dx, y + v.dy))
        if not side_v and not side_h:
            tiles.append((corner, v, h))
        elif not side_v:
            tiles.append((edge_v, v, h))
        elif not side_h:
            tiles.append((edge_h, v, h))
        elif not diagonal:
            tiles.append((inner, v, h))
    return tiles


def cell_at(map: Map, x: int, y: int) -> int:
    if 0 <= y < len(map) and 0 <= x < len(map[y]):
        return map[y][x]
    return 0
