from storage import Config
from models.world import respawn
from render import (
    FrameBuffer,
    Grid,
    draw_entities,
    draw_items,
    draw_maze,
    fit_grid,
    glyphs,
)
from systems import Outcome, step
from .base import Scene, Push, Transition, Reset
from scenes.factories import SceneFactories
from .pause import Pause
from assets import Assets, FontColor, Sprites
from models import Direction, Keys, new_map, new_world, next_level


class Gameplay(Scene):
    def __init__(
        self, factories: SceneFactories, config: Config, assets: Assets
    ) -> None:
        self.config = config
        self.assets = assets
        self.factories = factories
        self.world = new_world(new_map(), config.lives)

    def update(self, dt: float, keys: set[int]) -> Transition:
        if Keys.Escape in keys:
            return Push(Pause(self.assets))
        match step(self.world, self.config, dt, keys):
            case Outcome.LOST:
                score = self.world.score
                self.world = new_world(new_map(), self.config.lives)
                return Push(
                    self.factories.dead(self.config, self.assets, score)
                )
            case Outcome.DIED:
                self.world = respawn(self.world)
            case Outcome.WON:
                if self.world.level < self.config.levels_to_win:
                    self.world = next_level(self.world, new_map())
                    return None
                score = self.world.score
                self.world = new_world(new_map(), self.config.lives)
                return Reset(
                    self.factories.win(self.config, self.assets, score)
                )
        return None

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
        score = glyphs(f"Score {self.world.score}", font)
        level = glyphs(f"Level {self.world.level}", font)
        grid.put_row(score, 0, -1)
        grid.put_row(level, cols, -1, left_align=False)
        life = sprites.pacman[Direction.EAST][1]
        grid.put_row([life] * self.world.lives, 0, row)
