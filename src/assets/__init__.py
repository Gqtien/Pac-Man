from dataclasses import dataclass
from config import Config
from .font import Font, FontColor, Fonts, load_fonts
from .scaled import Scaled
from .sheet import SpriteSheet
from .sprites import Animation, Sprites, load_sprites


@dataclass(frozen=True)
class Assets:
    sprites: Scaled[Sprites]
    fonts: Scaled[Fonts]


def load_assets(config: Config) -> Assets:
    return Assets(
        Scaled(SpriteSheet.load(config.spritesheet, cell=16), load_sprites),
        Scaled(SpriteSheet.load(config.font, cell=8), load_fonts),
    )


__all__ = [
    "Animation",
    "Assets",
    "Font",
    "FontColor",
    "Fonts",
    "Scaled",
    "Sprites",
    "SpriteSheet",
    "load_assets",
]
