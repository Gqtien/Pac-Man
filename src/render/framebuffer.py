from PIL import Image


class FrameBuffer:
    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height
        self.canvas = Image.new("RGBA", (width, height))

    def clear(self, color: tuple[int, int, int, int] = (0, 0, 0, 255)) -> None:
        self.canvas.paste(color, (0, 0, self.width, self.height))

    def put_image(self, image: Image.Image, x: float, y: float) -> None:
        self.canvas.paste(image, (int(x), int(y)), image)
