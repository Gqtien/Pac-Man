import sys
from argparse import ArgumentParser
from pathlib import Path
from assets import load_assets
from storage import load_config
from scenes.factories import SceneFactories
from scenes import SceneManager, Main, Gameplay, Won, Lost, TimedOut
from functools import partial


def build_scenes() -> SceneFactories:
    s = SceneFactories()
    s.main = partial(Main, s)
    s.gameplay = partial(Gameplay, s)
    s.won = partial(Won, s)
    s.lost = partial(Lost, s)
    s.timed_out = partial(TimedOut, s)
    return s


def run() -> None:
    root = Path(__file__).resolve().parent.parent
    parser = ArgumentParser()
    parser.add_argument(
        "config",
        nargs="?",
        type=Path,
        default=root / "config.json",
        help="config file to load (default: %(default)s)",
    )
    args = parser.parse_args()
    config = load_config(args.config)
    assets = load_assets(root / "assets")
    factories = build_scenes()
    manager = SceneManager()
    manager.start(Main(factories, config, assets))


if __name__ == "__main__":
    try:
        run()
    except BaseException as e:
        sys.exit(f"Error: {e}")
