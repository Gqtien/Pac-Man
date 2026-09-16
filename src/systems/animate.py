from models import Entity


def animate(entity: Entity, speed: float, dt: float) -> None:
    entity.anim_progress += speed * dt
