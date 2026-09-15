from dataclasses import dataclass
from config import Config
from .font import Font, FontColor, Fonts, load_fonts
from .scaled import Scaled
from .sheet import SpriteSheet
from .sprites import Animation, Sprites, load_sprites
from .walls import (
    DOOR,
    FRAME,
    HOUSE_FRAME,
    RIM,
    Frame,
    Wall,
    Walls,
    load_walls,
)


@dataclass(frozen=True)
class Assets:
    sprites: Scaled[Sprites]
    fonts: Scaled[Fonts]
    walls: Scaled[Walls]


def load_assets(config: Config) -> Assets:
    return Assets(
        Scaled(SpriteSheet.load(config.spritesheet, cell=16), load_sprites),
        Scaled(SpriteSheet.load(config.font, cell=8), load_fonts),
        Scaled(SpriteSheet.load(config.walls, cell=8), load_walls),
    )


__all__ = [
    "Animation",
    "DOOR",
    "FRAME",
    "HOUSE_FRAME",
    "RIM",
    "Assets",
    "Font",
    "FontColor",
    "Fonts",
    "Frame",
    "Scaled",
    "Sprites",
    "SpriteSheet",
    "Wall",
    "Walls",
    "load_assets",
]
