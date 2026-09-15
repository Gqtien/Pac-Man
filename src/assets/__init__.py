from dataclasses import dataclass
from config import Config
from .font import Font, FontColor, Fonts, load_fonts
from .sheet import SpriteSheet
from .sprites import Animation, Sprites, load_sprites


@dataclass(frozen=True)
class Assets:
    sprites: Sprites
    fonts: Fonts


def load_assets(config: Config) -> Assets:
    return Assets(
        load_sprites(SpriteSheet(config.spritesheet, cell=16)),
        load_fonts(SpriteSheet(config.font, cell=8)),
    )


__all__ = [
    "Animation",
    "Assets",
    "Font",
    "FontColor",
    "Fonts",
    "Sprites",
    "SpriteSheet",
    "load_assets",
]
