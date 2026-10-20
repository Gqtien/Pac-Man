import shutil
from pathlib import Path
from PyInstaller.utils.hooks import collect_dynamic_libs

analysis = Analysis(
    ["src/__main__.py"],
    pathex=["src"],
    binaries=collect_dynamic_libs("mlx"),
)
exe = EXE(
    PYZ(analysis.pure),
    analysis.scripts,
    name="pacman",
    exclude_binaries=True,
)
COLLECT(exe, analysis.binaries, analysis.datas, name="pacman")

root = Path(SPECPATH)
game = Path(DISTPATH) / "pacman"
shutil.copytree(root / "assets", game / "assets")
shutil.copy(root / "config.json", game)
shutil.copytree(root / "package", game, dirs_exist_ok=True)
(game / "saves").mkdir()
