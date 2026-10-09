from pathlib import Path
from PIL import Image


def load_image(path: Path) -> Image.Image:
    with Image.open(path) as image:
        image.load()
    return image


class SpriteSheet:
    def __init__(self, image: Image.Image, cell: int) -> None:
        self.image = image
        self.cell = cell

    @classmethod
    def load(cls, path: Path, cell: int = 16) -> "SpriteSheet":
        return cls(load_image(path), cell)

    def zoom(self, scale: int) -> "SpriteSheet":
        return SpriteSheet(
            self.image.resize(
                (self.image.width * scale, self.image.height * scale),
                Image.Resampling.NEAREST
            ),
            self.cell * scale
        )

    def cut(self, x: int, y: int, w: int, h: int) -> Image.Image:
        return self.image.crop((x, y, x + w, y + h))

    def sprite(self, col: int, row: int) -> Image.Image:
        size = self.cell
        return self.cut(col * size, row * size, size, size)

    def sprites(self, cols: range, row: int) -> list[Image.Image]:
        return [self.sprite(col, row) for col in cols]
