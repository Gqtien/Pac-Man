from enum import Enum
from PIL.Image import Image
from typing import TypeAlias
from models import Direction
from .sheet import SpriteSheet


class Wall(Enum):
    EDGE_N = (14, 0)
    EDGE_S = (4, 1)
    EDGE_W = (9, 1)
    EDGE_E = (8, 1)
    CORNER_NW = (7, 1)
    CORNER_NE = (6, 1)
    CORNER_SW = (11, 1)
    CORNER_SE = (10, 1)
    INNER_NW = (5, 2)
    INNER_NE = (4, 2)
    INNER_SW = (3, 2)
    INNER_SE = (2, 2)

    HOUSE_NW = (13, 1)
    HOUSE_NE = (12, 1)
    HOUSE_SW = (15, 1)
    HOUSE_SE = (14, 1)
    HOUSE_INNER_NW = (12, 2)
    HOUSE_INNER_NE = (13, 2)
    HOUSE_INNER_SW = (14, 2)
    HOUSE_INNER_SE = (15, 2)
    RIM_N = (0, 3)
    RIM_S = (1, 3)
    RIM_W = (2, 3)
    RIM_E = (3, 3)
    RIM_NW = (4, 3)
    RIM_NE = (5, 3)
    RIM_SW = (6, 3)
    RIM_SE = (7, 3)
    RIM_INNER_NW = (8, 3)
    RIM_INNER_NE = (9, 3)
    RIM_INNER_SW = (10, 3)
    RIM_INNER_SE = (11, 3)

    DOOR_E_TOP = (12, 3)
    DOOR_E_BOTTOM = (13, 3)
    DOOR_W_TOP = (14, 3)
    DOOR_W_BOTTOM = (15, 3)


Walls: TypeAlias = dict[Wall, Image]

Frame: TypeAlias = dict[
    tuple[Direction, Direction],
    tuple[Wall, Wall, Wall, Wall],
]


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


def load_walls(sheet: SpriteSheet) -> Walls:
    return {wall: sheet.sprite(*wall.value) for wall in Wall}
