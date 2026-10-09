from typing import Callable, Generic, TypeVar
from PIL.Image import Image
from .sheet import SpriteSheet

Asset = TypeVar("Asset")


class Scaled(dict[int, Asset], Generic[Asset]):
    def __init__(
        self, sheet: SpriteSheet, load: Callable[[SpriteSheet], Asset]
    ) -> None:
        super().__init__()
        self.sheet = sheet
        self.load = load

    def __missing__(self, scale: int) -> Asset:
        asset = self[scale] = self.load(self.sheet.zoom(scale))
        return asset

    def fit(self, px: float) -> Asset:
        return self[max(1, int(px // self.sheet.cell))]


class Resized(dict[tuple[int, int], Image]):
    def __init__(self, image: Image) -> None:
        super().__init__()
        self.image = image

    def __missing__(self, size: tuple[int, int]) -> Image:
        image = self[size] = self.image.resize(size)
        return image
