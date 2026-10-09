from dataclasses import dataclass
from storage import Config
from .font import Font, FontColor, Fonts, load_fonts
from .scaled import Resized, Scaled
from .sheet import SpriteSheet, load_image
from .sprites import Animation, Sprites, load_sprites
from .walls import Wall, Walls, load_walls


@dataclass(frozen=True)
class Assets:
    sprites: Scaled[Sprites]
    fonts: Scaled[Fonts]
    walls: Scaled[Walls]
    overlay: Resized
    size: int = 16


def load_assets(config: Config) -> Assets:
    return Assets(
        Scaled(SpriteSheet.load(config.spritesheet, cell=16), load_sprites),
        Scaled(SpriteSheet.load(config.font, cell=8), load_fonts),
        Scaled(SpriteSheet.load(config.walls, cell=8), load_walls),
        Resized(load_image(config.overlay)),
    )


__all__ = [
    "Animation",
    "Assets",
    "Font",
    "FontColor",
    "Fonts",
    "Resized",
    "Scaled",
    "Sprites",
    "SpriteSheet",
    "Wall",
    "Walls",
    "load_assets",
]
