from dataclasses import dataclass
from tkinter import PhotoImage
from typing import TypeAlias
from models import Direction, GhostPersonality
from .sheet import SpriteSheet

Animation: TypeAlias = list[PhotoImage]


@dataclass(frozen=True)
class Sprites:
    pacman: dict[Direction, Animation]
    death: Animation
    ghost: dict[GhostPersonality, dict[Direction, Animation]]
    frightened: Animation
    flashing: Animation
    eyes: dict[Direction, PhotoImage]
    ghost_score: dict[int, PhotoImage]


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
                Direction.NONE: sheet.sprites(range(0, 2), row),
                Direction.EAST: sheet.sprites(range(0, 2), row),
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
    )
