from argparse import ArgumentParser
from pathlib import Path
from assets import load_assets
from storage import load_config
from scenes.factories import SceneFactories
from scenes import SceneManager, Main, Gameplay, Won, Lost
from functools import partial


def build_scenes() -> SceneFactories:
    s = SceneFactories()
    s.main = partial(Main, s)
    s.gameplay = partial(Gameplay, s)
    s.won = partial(Won, s)
    s.lost = partial(Lost, s)
    return s


def run() -> None:
    parser = ArgumentParser()
    parser.add_argument(
        "config",
        nargs="?",
        type=Path,
        default=Path("config.json"),
        help="config file to load (default: %(default)s)",
    )
    args = parser.parse_args()
    manager = SceneManager()
    config = load_config(args.config)
    assets = load_assets(config)
    factories = build_scenes()
    manager.start(Main(factories, config, assets))


if __name__ == "__main__":
    run()
