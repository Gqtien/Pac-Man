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
        self, images: list[Image], col: int, row: int, left_align: bool = True
    ) -> None:
        width, height = images_size(images)
        x = self.left + col * self.cell_size - (0 if left_align else width)
        y = self.top + row * self.cell_size + (self.cell_size - height) // 2
        put_images(images, self.framebuffer, x, y)

    def offset(self, cols: int, rows: int) -> "Grid":
        return replace(
            self,
            left=self.left + cols * self.cell_size,
            top=self.top + rows * self.cell_size,
        )


def fit_grid(
    framebuffer: FrameBuffer, cols: int, rows: int, size: int
) -> tuple[Grid, int]:
    scale = max(
        1,
        min(
            framebuffer.width // (size * cols),
            framebuffer.height // (size * rows),
        ),
    )
    cell_size = size * scale
    left = (framebuffer.width - cols * cell_size) // 2
    top = (framebuffer.height - rows * cell_size) // 2
    return Grid(framebuffer, cell_size, left, top), scale
