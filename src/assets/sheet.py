from PIL.Image import Image
import PIL


class SpriteSheet:
    def __init__(self, image: Image, cell: int) -> None:
        self.image = image
        self.cell = cell

    @classmethod
    def load(cls, path: str, cell: int) -> "SpriteSheet":
        with PIL.Image.open(path) as img:
            img.load()
        return cls(img, cell)

    def zoom(self, scale: int) -> "SpriteSheet":
        return SpriteSheet(
            self.image.resize(
                (self.image.width * scale, self.image.height * scale),
                PIL.Image.Resampling.NEAREST
            ),
            self.cell * scale
        )

    def cut(self, x: int, y: int, w: int, h: int) -> Image:
        return self.image.crop((x, y, x + w, y + h))

    def sprite(self, col: int, row: int) -> Image:
        size = self.cell
        return self.cut(col * size, row * size, size, size)

    def sprites(self, cols: range, row: int) -> list[Image]:
        return [self.sprite(col, row) for col in cols]
