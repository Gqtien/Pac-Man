from enum import Enum
from typing import TypeAlias
from .map import Map, is_solid


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


Items: TypeAlias = dict[tuple[int, int], Item]


def init_items(map: Map) -> Items:
    items: Items = {}
    for pacgum in pacgums(map):
        items[pacgum] = Item.PACGUM
    for superpacgum in superpacgums(map):
        items[superpacgum] = Item.SUPER_PACGUM
    return items


def pacgums(map: Map) -> list[tuple[int, int]]:
    pacgums: list[tuple[int, int]] = []
    for y, row in enumerate(map):
        for x, tile in enumerate(row):
            if not is_solid(tile):
                pacgums.append((x, y))
    return pacgums


def superpacgums(map: Map) -> list[tuple[int, int]]:
    offset = 1
    return [
        (offset * 2 + 1, offset * 2 + 1),
        (len(map) - (offset * 2 + 2), offset * 2 + 1),
        (offset * 2 + 1, len(map) - (offset * 2 + 2)),
        (len(map) - (offset * 2 + 2), len(map) - (offset * 2 + 2)),
    ]
