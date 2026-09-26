from dataclasses import dataclass
from typing import TypeAlias
from models import Direction, GhostPersonality, Item
from .sheet import SpriteSheet
from PIL.Image import Image

Animation: TypeAlias = list[Image]


@dataclass(frozen=True)
class Sprites:
    pacman: dict[Direction, Animation]
    death: Animation
    ghost: dict[GhostPersonality, dict[Direction, Animation]]
    frightened: Animation
    flashing: Animation
    eyes: dict[Direction, Image]
    ghost_score: dict[int, Image]
    items: dict[Item, Image]


def load_sprites(sheet: SpriteSheet) -> Sprites:
    return Sprites(
        pacman={
            Direction.NONE: sheet.sprites(range(2, 3), 0),
            Direction.EAST: sheet.sprites(range(3), 0),
            Direction.WEST: sheet.sprites(range(3), 1),
            Direction.NORTH: sheet.sprites(range(3), 2),
            Direction.SOUTH: sheet.sprites(range(3), 3),
        },
        death=sheet.sprites(range(3, 14), 0),
        ghost={
            personality: {
                Direction.NONE: sheet.sprites(range(2), row),
                Direction.EAST: sheet.sprites(range(2), row),
                Direction.WEST: sheet.sprites(range(2, 4), row),
                Direction.NORTH: sheet.sprites(range(4, 6), row),
                Direction.SOUTH: sheet.sprites(range(6, 8), row),
            }
            for row, personality in enumerate(GhostPersonality, start=4)
        },
        frightened=sheet.sprites(range(8, 10), 4),
        flashing=sheet.sprites(range(10, 12), 4),
        eyes={
            Direction.NONE: sheet.sprite(8, 5),
            Direction.EAST: sheet.sprite(8, 5),
            Direction.WEST: sheet.sprite(9, 5),
            Direction.NORTH: sheet.sprite(10, 5),
            Direction.SOUTH: sheet.sprite(11, 5),
        },
        ghost_score={
            200: sheet.sprite(0, 8),
            400: sheet.sprite(1, 8),
            800: sheet.sprite(2, 8),
            1600: sheet.sprite(3, 8),
        },
        items={
            Item.CHERRIES: sheet.sprite(3, 3),
            Item.STRAWBERRY: sheet.sprite(4, 3),
            Item.PEACH: sheet.sprite(5, 3),
            Item.APPLE: sheet.sprite(6, 3),
            Item.GRAPES: sheet.sprite(7, 3),
            Item.GALAXIAN: sheet.sprite(8, 3),
            Item.BELL: sheet.sprite(9, 3),
            Item.KEY: sheet.sprite(10, 3),
            Item.PACGUM: sheet.sprite(11, 3),
            Item.SUPER_PACGUM: sheet.sprite(12, 3),
        },
    )
