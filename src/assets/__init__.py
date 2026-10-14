from dataclasses import dataclass
from pathlib import Path
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


def load_assets(folder: Path) -> Assets:
    return Assets(
        Scaled(SpriteSheet.load(folder / "spritesheet.png"), load_sprites),
        Scaled(SpriteSheet.load(folder / "font.png", cell=8), load_fonts),
        Scaled(SpriteSheet.load(folder / "walls.png", cell=8), load_walls),
        Resized(load_image(folder / "pause_overlay.png")),
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
