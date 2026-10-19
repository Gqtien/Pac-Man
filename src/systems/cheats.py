from storage import Config
from models import Cheat, Game


def step(game: Game, config: Config, keys: set[int]) -> None:
    if config.cheat_win_key in keys:
        game.level.items.clear()
    toggles = (
        (config.cheat_invincible_key, Cheat.INVINCIBLE),
        (config.cheat_freeze_ghosts_key, Cheat.FREEZE_GHOSTS),
    )
    for key, cheat in toggles:
        if key in keys:
            game.cheats ^= {cheat}
