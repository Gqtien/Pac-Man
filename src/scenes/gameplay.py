import math
from assets import Assets, FontColor, Sprites
from models import Direction, Keys, new_game
from render import (
    FrameBuffer,
    Grid,
    MazeLayer,
    draw_entities,
    draw_items,
    fit_grid,
    glyphs,
)
from storage import Config
from systems import step
from .base import Scene
from .events import Event, Finish, Pause


class Gameplay(Scene):
    def __init__(self, config: Config, assets: Assets) -> None:
        self.config = config
        self.assets = assets
        self.game = new_game(config.lives)
        self.maze = MazeLayer()

    def update(self, dt: float, keys: set[int]) -> Event:
        if Keys.Escape in keys:
            return Pause()
        if (outcome := step(self.game, self.config, dt, keys)) is not None:
            return Finish(self.game.score, outcome)
        return None

    def draw(self, framebuffer: FrameBuffer) -> None:
        level, assets = self.game.level, self.assets
        rows, cols = len(level.map), len(level.map[0])
        grid = fit_grid(framebuffer, cols, rows + 2).offset(0, 1)
        sprites = assets.sprites[grid.cell_size]
        framebuffer.clear()
        self.maze.draw(grid, level.map, assets.walls[grid.cell_size // 2])
        draw_items(grid, level.items, sprites)
        draw_entities(grid, level, sprites)
        self.draw_hud(grid, sprites, cols, rows)

    def draw_hud(
        self, grid: Grid, sprites: Sprites, cols: int, row: int
    ) -> None:
        font = self.assets.fonts.fit(grid.cell_size / 2)[FontColor.WHITE]
        remaining = self.config.level_time_limit - self.game.level.timer
        score = glyphs(f"Score {self.game.score}", font)
        timer = glyphs(self.format_time(remaining), font)
        level = glyphs(f"Level {self.game.level.number}", font)
        grid.put_row(score, 0, -1)
        grid.put_row(timer, cols / 2, -1, align=0.5)
        grid.put_row(level, cols, -1, align=1)
        life = sprites.pacman[Direction.EAST][1]
        grid.put_row([life] * self.game.lives, 0, row)

    @staticmethod
    def format_time(seconds: float) -> str:
        m, s = divmod(math.ceil(seconds), 60)
        return f"{m}:{s:02}"
