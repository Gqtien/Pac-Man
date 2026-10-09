from PIL.Image import Image
from .framebuffer import FrameBuffer


def images_size(images: list[Image]) -> tuple[int, int]:
    width = sum(image.width for image in images)
    height = max((image.height for image in images), default=0)
    return width, height


def put_images(
    images: list[Image], framebuffer: FrameBuffer, x: int, y: int
) -> None:
    for image in images:
        framebuffer.put_image(image, x, y)
        x += image.width
