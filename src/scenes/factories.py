from typing import Callable
from .base import Scene


class SceneFactories:
    main:      Callable[..., Scene]
    gameplay:  Callable[..., Scene]
    won:       Callable[..., Scene]
    lost:      Callable[..., Scene]
    timed_out: Callable[..., Scene]
