from PIL.Image import Image
from mlx import Mlx


class FrameBuffer:
    def __init__(self, mlx: Mlx, image: int) -> None:
        self.origin: tuple[int, int] = 0, 0
        self.data: memoryview
        self.bits_per_pixel: int
        self.size_line: int
        self.endianness: int  # 0 -> BGRA    1 -> ARGB
        self.data, self.bits_per_pixel, self.size_line, self.endianness = \
            mlx.mlx_get_data_addr(image)
        self.bytes_per_pixel: int = self.bits_per_pixel // 8

    @property
    def width(self) -> int:
        return self.size_line // self.bytes_per_pixel

    @property
    def height(self) -> int:
        return self.data.nbytes // self.size_line

    def put_pixel(self, x: int, y: int, color: bytes) -> None:
        x += self.origin[0]
        y += self.origin[1]
        offset = y * self.size_line + x * self.bytes_per_pixel
        print(self.data[offset:offset + self.bytes_per_pixel])
        self.data[offset:offset + self.bytes_per_pixel] = color

    def put_line(self, x: int, y: int, width: int, color: bytes) -> None:
        x += self.origin[0]
        y += self.origin[1]
        offset = y * self.size_line + x * self.bytes_per_pixel
        self.data[offset:offset + width * self.bytes_per_pixel] = color * width

    def clear(self, color: bytes) -> None:
        self.data[:] = color * (self.data.nbytes // self.bytes_per_pixel)

    def move(self, dx: int, dy: int) -> None:
        self.origin = self.origin[0] + dx, self.origin[1] + dy

    def put_image(self, image: Image, x: int | float, y: int | float) -> None:
        x += self.origin[0]
        y += self.origin[1]
        x,  y = int(x), int(y)
        img_bytes: bytes = image.convert("RGBA").tobytes("raw", "BGRA", 0, 1)
        row_bytes_len: int = image.width * 4

        for iy in range(image.height):
            src_off: int = iy * row_bytes_len
            dst_off: int = (y + iy) * self.size_line + x * self.bytes_per_pixel

            row = bytes(img_bytes[src_off:src_off + row_bytes_len])
            self.data[dst_off:dst_off + row_bytes_len] = row
