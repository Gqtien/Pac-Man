import math
from pathlib import Path
from PIL import Image


def load_image(path: Path) -> Image.Image:
    with Image.open(path) as image:
        return image.convert("RGBA")


class SpriteSheet:
    def __init__(self, image: Image.Image, cell: int) -> None:
        self.image = image
        self.cell = cell

    @classmethod
    def load(cls, path: Path, cell: int = 16) -> "SpriteSheet":
        return cls(load_image(path), cell)

    def zoom(self, cell: int) -> "SpriteSheet":
        cols = self.image.width // self.cell
        rows = self.image.height // self.cell
        image = Image.new("RGBA", (cols * cell, rows * cell))
        for row in range(rows):
            for col in range(cols):
                sprite = resize_sprite(self.sprite(col, row), cell)
                image.paste(sprite, (col * cell, row * cell))
        return SpriteSheet(image, cell)

    def cut(self, x: int, y: int, w: int, h: int) -> Image.Image:
        return self.image.crop((x, y, x + w, y + h))

    def sprite(self, col: int, row: int) -> Image.Image:
        size = self.cell
        return self.cut(col * size, row * size, size, size)

    def sprites(self, cols: range, row: int) -> list[Image.Image]:
        return [self.sprite(col, row) for col in cols]


def resize_sprite(image: Image.Image, size: int) -> Image.Image:
    factor = math.ceil(size / image.width)
    sharp = image.resize(
        (image.width * factor, image.height * factor),
        Image.Resampling.NEAREST,
    )
    return sharp.resize((size, size), Image.Resampling.BOX)
