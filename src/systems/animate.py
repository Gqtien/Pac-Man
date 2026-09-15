from config import Config
from models import Entity, World


def animate(entity: Entity, world: World, config: Config, dt: float) -> None:
    entity.anim_progress += config.anim_speed * dt
    # if entity.anim_progress >= 1.0:
    #     entity.anim_progress -= 1.0
