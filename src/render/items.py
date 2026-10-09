from assets import Sprites
from models import Items
from .grid import Grid


def draw_items(grid: Grid, items: Items, sprites: Sprites) -> None:
    for pos, item in items.items():
        grid.put(sprites.items[item], *pos)
