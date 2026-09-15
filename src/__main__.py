import argparse
from pathlib import Path
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
    manager.start(Gameplay(load_config(args.config)))


if __name__ == "__main__":
    run()
