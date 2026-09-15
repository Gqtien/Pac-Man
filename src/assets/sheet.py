from tkinter import PhotoImage


class SpriteSheet:
    def __init__(self, image: PhotoImage, cell: int) -> None:
        self.image = image
        self.cell = cell

    @classmethod
    def load(cls, path: str, cell: int) -> "SpriteSheet":
        return cls(PhotoImage(file=path), cell)

    def zoom(self, scale: int) -> "SpriteSheet":
        return SpriteSheet(self.image.zoom(scale), self.cell * scale)

    def cut(self, x: int, y: int, w: int, h: int) -> PhotoImage:
        sprite = PhotoImage(width=w, height=h)
        sprite.tk.call(sprite, "copy", self.image, "-from", x, y, x + w, y + h)
        return sprite

    def sprite(self, col: int, row: int) -> PhotoImage:
        size = self.cell
        return self.cut(col * size, row * size, size, size)

    def sprites(self, cols: range, row: int) -> list[PhotoImage]:
        return [self.sprite(col, row) for col in cols]
