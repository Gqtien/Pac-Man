import sys
from argparse import ArgumentParser
from pathlib import Path
from assets import load_assets
from render import Window
from scenes import Router, SceneManager
from storage import load_config


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
    window = Window("PacMan")
    router = Router(config, assets)
    SceneManager(window, router).run()


if __name__ == "__main__":
    try:
        run()
    except Exception as e:
        sys.exit(f"Error: {e}")
