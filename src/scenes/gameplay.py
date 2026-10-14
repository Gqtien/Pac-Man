import math
from typing import Callable
from .base import Scene, Push, Transition, Reset
from .factories import SceneFactories
from .pause import Pause
from storage import Config
from systems import Outcome, step
from assets import Assets, FontColor, Sprites
from models import Direction, Keys, new_map, new_world, next_level, respawn
from render import (
    FrameBuffer,
    Grid,
    draw_entities,
    draw_items,
    draw_maze,
    fit_grid,
    glyphs,
)


class Gameplay(Scene):
    def __init__(
        self, factories: SceneFactories, config: Config, assets: Assets
    ) -> None:
        self.config = config
        self.assets = assets
        self.factories = factories
        self.world = new_world(new_map(seed=42), config.lives)

    def update(self, dt: float, keys: set[int]) -> Transition:
        if Keys.Escape in keys:
            return Push(Pause(self.factories, self.config, self.assets))
        match step(self.world, self.config, dt, keys):
            case Outcome.DIED:
                self.world = respawn(self.world)
            case Outcome.WON if self.world.level < self.config.levels_to_win:
                self.world = next_level(self.world, new_map())
            case Outcome.WON:
                return self.end(self.factories.won)
            case Outcome.LOST:
                return self.end(self.factories.lost)
            case Outcome.TIMED_OUT:
                return self.end(self.factories.timed_out)
        return None

    def end(self, scene: Callable[..., Scene]) -> Transition:
        return Reset(scene(self.config, self.assets, self.world.score))

    def draw(self, framebuffer: FrameBuffer) -> None:
        world, assets = self.world, self.assets
        rows, cols = len(world.map), len(world.map[0])
        screen, scale = fit_grid(framebuffer, cols, rows + 2, assets.size)
        grid = screen.offset(0, 1)
        sprites = assets.sprites[scale]
        framebuffer.clear()
        draw_maze(grid, world.map, assets.walls[scale])
        draw_items(grid, world.items, sprites)
        draw_entities(grid, world, sprites)
        self.draw_hud(grid, sprites, cols, rows)

    def draw_hud(
        self, grid: Grid, sprites: Sprites, cols: int, row: int
    ) -> None:
        font = self.assets.fonts.fit(grid.cell_size / 2)[FontColor.WHITE]
        remaining = self.config.level_time_limit - self.world.timer
        score = glyphs(f"Score {self.world.score}", font)
        timer = glyphs(self.format_time(remaining), font)
        level = glyphs(f"Level {self.world.level}", font)
        grid.put_row(score, 0, -1)
        grid.put_row(timer, cols / 2, -1, align=0.5)
        grid.put_row(level, cols, -1, align=1)
        life = sprites.pacman[Direction.EAST][1]
        grid.put_row([life] * self.world.lives, 0, row)

    @staticmethod
    def format_time(seconds: float) -> str:
        m, s = divmod(math.ceil(seconds), 60)
        return f"{m}:{s:02}"
