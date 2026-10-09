from .config import Config, load_config
from .highscores import Highscores, load_highscores, save_score

__all__ = [
    "Config",
    "Highscores",
    "load_config",
    "load_highscores",
    "save_score",
]
