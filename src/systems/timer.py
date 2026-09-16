def spend(timer: float, dt: float) -> tuple[float, float]:
    used = min(timer, dt)
    return timer - used, dt - used
