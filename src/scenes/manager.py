import sys
from models import FrameBuffer
import time
from .base import Scene, Pop, Push, Reset, Transition
from mlx import Mlx


class SceneManager:
    def __init__(self) -> None:
        self.mlx: Mlx = Mlx()
        mlx_ptr = self.mlx.mlx_init()
        if mlx_ptr is None:
            print("failed to init mlx", file=sys.stderr)
            sys.exit(1)
        self.mlx_ptr: int = mlx_ptr

        _, width, height = self.mlx.mlx_get_screen_size(self.mlx_ptr)
        window = self.mlx.mlx_new_window(
            self.mlx_ptr, width, height, "pacman"
        )
        if window is None:
            print("failed to init window", file=sys.stderr)
            sys.exit(1)
        self.window: int = window
        img_a = self.mlx.mlx_new_image(self.mlx_ptr, width, height)
        img_b = self.mlx.mlx_new_image(self.mlx_ptr, width, height)
        if img_a is None or img_b is None:
            print("failed to init image", file=sys.stderr)
            sys.exit(1)
        self.image_a: int = img_a
        self.image_b: int = img_b

        self.stack: list[Scene] = []
        self.last: float = time.perf_counter()
        self.keys: set[str] = set()

        self.mlx.mlx_key_hook(self.window, self.on_key, None)
        self.mlx.mlx_loop_hook(self.mlx_ptr, self.tick, None)

    def start(self, initial_scene: Scene) -> None:
        self.initial_scene = initial_scene
        self.stack.append(initial_scene)
        self.mlx.mlx_loop(self.mlx_ptr)

    @property
    def top(self) -> Scene:
        return self.stack[-1]

    def on_key(self, keycode: int, _: None) -> None:
        print(keycode)
        key = chr(keycode)
        match keycode:
            case 65307:
                key = "Return"
            case 65293:
                key = "Return"
            case 65288:
                key = "BackSpace"
        self.keys.add(key)

    def tick(self, _: None) -> None:
        if not self.stack:
            self.mlx.mlx_release(self.mlx_ptr)
            return

        now = time.perf_counter()
        dt, self.last = now - self.last, now
        keys, self.keys = self.keys, set()

        framebuffer = FrameBuffer(self.mlx, self.image_a)

        transition: Transition = self.top.update(dt, keys)
        self.apply(transition)
        self.top.draw(framebuffer)
        # for scene in self.stack:
        #     scene.draw(framebuffer)

        self.mlx.mlx_clear_window(self.mlx_ptr, self.window)
        self.mlx.mlx_put_image_to_window(
            self.mlx_ptr, self.window, self.image_a, 0, 0
        )
        self.image_a, self.image_b = self.image_b, self.image_a

    def apply(self, transition: Transition) -> None:
        match transition:
            case Push():
                self.stack.append(transition.scene)
            case Pop():
                self.stack.pop()
            case Reset():
                self.stack = [transition.scene]
            case None:
                pass
