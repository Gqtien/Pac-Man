from dataclasses import dataclass, replace
from PIL.Image import Image
from .framebuffer import FrameBuffer
from .images import images_size, put_images


@dataclass(frozen=True)
class Grid:
    framebuffer: FrameBuffer
    cell_size: int
    left: int
    top: int

    def put(self, image: Image, x: float, y: float) -> None:
        px = self.left + x * self.cell_size
        py = self.top + y * self.cell_size
        self.framebuffer.put_image(image, px, py)

    def put_row(
        self, images: list[Image], col: float, row: int, align: float = 0
    ) -> None:
        width, height = images_size(images)
        x = self.left + int(col * self.cell_size - width * align)
        y = self.top + row * self.cell_size + (self.cell_size - height) // 2
        put_images(images, self.framebuffer, x, y)

    def offset(self, cols: int, rows: int) -> "Grid":
        return replace(
            self,
            left=self.left + cols * self.cell_size,
            top=self.top + rows * self.cell_size,
        )


def fit_grid(framebuffer: FrameBuffer, cols: int, rows: int) -> Grid:
    cell = min(framebuffer.width // cols, framebuffer.height // rows)
    cell = max(2, cell - cell % 2)
    left = (framebuffer.width - cols * cell) // 2
    top = (framebuffer.height - rows * cell) // 2
    return Grid(framebuffer, cell, left, top)
