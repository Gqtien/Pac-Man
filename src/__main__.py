import argparse
from pathlib import Path
from assets import load_assets
from config import load_config
from scenes import Gameplay, SceneManager


def run() -> None:
    parser = argparse.ArgumentParser()
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
    manager.start(Gameplay(config, assets))


if __name__ == "__main__":
    run()
