import time
from collections.abc import Callable
from mlx import Mlx
from render import FrameBuffer


class Window:
    def __init__(self, title: str) -> None:
        self.mlx = Mlx()
        self.ptr = self.mlx.mlx_init()
        _, w, h = self.mlx.mlx_get_screen_size(self.ptr)
        self.window = self.mlx.mlx_new_window(self.ptr, w, h, title)
        self.images = []
        for _ in range(2):
            image = self.mlx.mlx_new_image(self.ptr, w, h)
            self.images.append((image, self.mlx.mlx_get_data_addr(image)[0]))
        _, bits, size_line, _ = self.mlx.mlx_get_data_addr(self.images[0][0])
        self.width = size_line // (bits // 8)
        self.height = h
        self.mlx.mlx_hook(self.window, 33, 0, lambda _: self.close(), None)

    def run(
        self,
        frame: Callable[[], None],
        key: Callable[[int], None],
    ) -> None:
        self.mlx.mlx_hook(self.window, 2, 1, lambda code, _: key(code), None)
        self.mlx.mlx_loop_hook(self.ptr, lambda _: self.paced(frame), None)
        self.mlx.mlx_loop(self.ptr)
        self.release()

    def paced(self, frame: Callable[[], None]) -> None:
        start = time.perf_counter()
        frame()
        time.sleep(max(0.0, 1 / 60 - (time.perf_counter() - start)))

    def show(self, framebuffer: FrameBuffer) -> None:
        image, pixels = self.images[0]
        pixels[:] = framebuffer.canvas.tobytes("raw", "BGRA")
        self.mlx.mlx_put_image_to_window(self.ptr, self.window, image, 0, 0)
        self.images.reverse()

    def close(self) -> None:
        self.mlx.mlx_loop_exit(self.ptr)

    def release(self) -> None:
        for image, _ in self.images:
            self.mlx.mlx_destroy_image(self.ptr, image)
        self.mlx.mlx_destroy_window(self.ptr, self.window)
        self.mlx.mlx_release(self.ptr)
