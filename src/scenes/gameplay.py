from tkinter import Canvas
from mazegenerator import MazeGenerator
from assets import Animation, Assets, Sprites
from config import Config
from systems import Outcome, step
from .base import Scene
from .death import Death
from .main import Main
from .pause import Pause
from .transition import Push, Reset, Transition
from models import (
    Color,
    Direction,
    Entity,
    Ghost,
    GhostPersonality,
    GhostState,
    Map,
    Pacman,
    Vec2,
    World,
    from_maze,
    open_sides,
)


class Gameplay(Scene):
    def __init__(self, config: Config, assets: Assets) -> None:
        self.config = config
        self.assets = assets
        self.world = World(
            from_maze(MazeGenerator().maze),
            Pacman(Vec2(1, 1), Direction.NONE),
            [
                Ghost(Vec2(11, 1), Direction.NONE, GhostPersonality.BLINKY),
                Ghost(Vec2(11, 3), Direction.NONE, GhostPersonality.PINKY),
                Ghost(Vec2(11, 5), Direction.NONE, GhostPersonality.INKY),
                Ghost(Vec2(11, 7), Direction.NONE, GhostPersonality.CLYDE),
            ],
        )

    def update(self, dt: float, keys: set[str]) -> Transition:
        if "Escape" in keys:
            return Push(Pause(self.config, self.assets))
        match step(self.world, self.config, dt, keys):
            case Outcome.LOST:
                return Push(Death())
            case Outcome.WON:
                return Reset(Main())
            case _:
                return None

    def draw(self, canvas: Canvas) -> None:
        size: float = self.cell_size(self.world.map, canvas)
        sprites: Sprites = self.assets.sprites.fit(size)
        # map
        self.draw_map(self.world.map, size, canvas)

        # pacman
        anim: Animation = sprites.pacman[self.world.pacman.direction]
        self.animate_entity(self.world.pacman, anim, size, canvas)

        # ghosts
        for ghost in self.world.ghosts:
            anim = self.ghost_animation(ghost, sprites)
            self.animate_entity(ghost, anim, size, canvas)

        self.center(self.world.map, size, canvas)

    @staticmethod
    def cell_size(map: Map, canvas: Canvas) -> float:
        rows, cols = len(map), len(map[0])
        return min(canvas.winfo_width() / cols, canvas.winfo_height() / rows)

    @staticmethod
    def center(map: Map, size: float, canvas: Canvas) -> None:
        rows, cols = len(map), len(map[0])
        dx = (canvas.winfo_width() - cols * size) / 2
        dy = (canvas.winfo_height() - rows * size) / 2
        canvas.move("all", dx, dy)

    @staticmethod
    def ghost_animation(ghost: Ghost, sprites: Sprites) -> Animation:
        match ghost.state:
            case GhostState.CHASE | GhostState.SCATTER:
                return sprites.ghost[ghost.personality][ghost.direction]
            case GhostState.DEAD:
                return [sprites.eyes[ghost.direction]]
            case GhostState.FRIGHTENED:
                return sprites.frightened

    @staticmethod
    def animate_entity(
        entity: Entity, animation: Animation, size: float, canvas: Canvas
    ) -> None:
        x = (entity.pos.x + entity.direction.dx * entity.progress + 0.5) * size
        y = (entity.pos.y + entity.direction.dy * entity.progress + 0.5) * size
        canvas.create_image(
            (x, y),
            image=animation[int(entity.anim_progress) % len(animation)],
        )

    @staticmethod
    def draw_map(map: Map, size: float, canvas: Canvas) -> None:
        for y, line in enumerate(map):
            for x, cell in enumerate(line):
                if not cell:
                    continue
                px = size * x
                py = size * y
                canvas.create_rectangle(
                    px, py, px + size, py + size, fill=Color.WALL, width=0
                )
                for direction in open_sides(cell):
                    Gameplay.draw_edge(px, py, size, direction, canvas)

    @staticmethod
    def draw_edge(
        px: float, py: float, size: float, direction: Direction, canvas: Canvas
    ) -> None:
        half = size / 2
        mx = px + half + direction.dx * half
        my = py + half + direction.dy * half
        canvas.create_line(
            mx - direction.dy * half,
            my - direction.dx * half,
            mx + direction.dy * half,
            my + direction.dx * half,
            fill=Color.WALL_OUTLINE,
        )
