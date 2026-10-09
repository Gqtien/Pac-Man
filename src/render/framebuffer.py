from PIL import Image
from mlx import Mlx


class FrameBuffer:
    def __init__(self, mlx: Mlx, image: int) -> None:
        self.data: memoryview
        self.bits_per_pixel: int
        self.size_line: int
        self.endianness: int  # 0 -> BGRA    1 -> ARGB
        self.data, self.bits_per_pixel, self.size_line, self.endianness = (
            mlx.mlx_get_data_addr(image)
        )
        self.bytes_per_pixel: int = self.bits_per_pixel // 8
        self.canvas = Image.new("RGBA", (self.width, self.height))

    @property
    def width(self) -> int:
        return self.size_line // self.bytes_per_pixel

    @property
    def height(self) -> int:
        return self.data.nbytes // self.size_line

    def clear(self, color: tuple[int, int, int, int] = (0, 0, 0, 255)) -> None:
        self.canvas.paste(color, (0, 0, self.width, self.height))

    def put_image(self, image: Image.Image, x: float, y: float) -> None:
        self.canvas.paste(image, (int(x), int(y)), image)

    def flush(self) -> None:
        self.data[:] = self.canvas.tobytes("raw", "BGRA")
