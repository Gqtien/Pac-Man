from tkinter import PhotoImage


class SpriteSheet:
    def __init__(self, path: str, cell: int) -> None:
        self.image = PhotoImage(file=path)
        self.cell = cell

    def cut(self, x: int, y: int, w: int, h: int) -> PhotoImage:
        sprite = PhotoImage(width=w, height=h)
        sprite.tk.call(sprite, "copy", self.image, "-from", x, y, x + w, y + h)
        return sprite

    def sprite(self, col: int, row: int) -> PhotoImage:
        size = self.cell
        return self.cut(col * size, row * size, size, size)

    def sprites(self, cols: range, row: int) -> list[PhotoImage]:
        return list(self.sprite(col, row) for col in cols)
