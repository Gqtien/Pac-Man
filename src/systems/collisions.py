from config import Config
from models import World


def step(world: World, config: Config) -> None:
    eat(world)

def eat(world: World) -> None:
    pos = world.pacman.pos
    item = world.items.pop((pos.x, pos.y), None)
    if item is not None:
        world.score += item.value
