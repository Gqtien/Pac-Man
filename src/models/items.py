from enum import Enum
from typing import TypeAlias
from .map import Map, is_solid
from .vec import Vec2


class Item(Enum):
    PACGUM = 1
    SUPER_PACGUM = 50
    CHERRIES = 100
    STRAWBERRY = 300
    PEACH = 500
    APPLE = 700
    GRAPES = 1000
    GALAXIAN = 2000
    BELL = 3000
    KEY = 5000

    @property
    def stall(self) -> float:
        frame = 1 / 60
        match self:
            case Item.PACGUM:
                return frame
            case Item.SUPER_PACGUM:
                return 3 * frame
            case _:
                return 0


Items: TypeAlias = dict[Vec2, Item]


def init_items(map: Map) -> Items:
    items: Items = {}
    for pacgum in pacgums(map):
        items[pacgum] = Item.PACGUM
    for superpacgum in superpacgums(map):
        items[superpacgum] = Item.SUPER_PACGUM
    return items


def pacgums(map: Map) -> list[Vec2]:
    pacgums: list[Vec2] = []
    for y, row in enumerate(map):
        for x, tile in enumerate(row):
            if not is_solid(tile):
                pacgums.append(Vec2(x, y))
    return pacgums


def superpacgums(map: Map) -> list[Vec2]:
    offset = 1
    return [
        Vec2(offset * 2 + 1, offset * 2 + 1),
        Vec2(len(map) - (offset * 2 + 2), offset * 2 + 1),
        Vec2(offset * 2 + 1, len(map) - (offset * 2 + 2)),
        Vec2(len(map) - (offset * 2 + 2), len(map) - (offset * 2 + 2)),
    ]
