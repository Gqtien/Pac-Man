from models import Entity, World


def animate(entity: Entity, world: World, dt: float) -> None:
    entity.anim_progress += world.config.anim_speed * dt
    # if entity.anim_progress >= 1.0:
    #     entity.anim_progress -= 1.0
