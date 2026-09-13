from tkinter import Canvas
from config import Config
from mazegenerator import MazeGenerator
import systems
from systems import Outcome
from .base import Scene
from .death import Death
from .main import Main
from .pause import Pause
from .transition import Push, Reset, Transition
from models import (
    Direction,
    Entity,
    Ghost,
    Pacman,
    GhostPersonality,
    Vec2,
    World,
    Color,
    Map,
)
from utils import (
    WALL_NORTH,
    WALL_EAST,
    WALL_SOUTH,
    WALL_WEST,
    maze_to_grid,
    grid_to_walls,
)


class Gameplay(Scene):
    def __init__(self, config: Config) -> None:
        self.world = World(
            grid_to_walls(maze_to_grid(MazeGenerator().maze)),
            Pacman(Vec2(1, 1), Direction.NONE),
            [Ghost(Vec2(11, 1), Direction.NONE, GhostPersonality.BLINKY)],
            config,
        )

    def update(self, dt: float, keys: set[str]) -> Transition:
        if "Escape" in keys:
            return Push(Pause())
        match systems.step(self.world, dt, keys):
            case Outcome.LOST:
                return Push(Death())
            case Outcome.WON:
                return Reset(Main())
            case _:
                return None

    def draw(self, canvas: Canvas) -> None:
        size: float = self.cell_size(self.world.map, canvas)
        canvas.delete("all")
        self.draw_map(self.world.map, size, canvas)
        self.draw_entity(self.world.pacman, Color.PACMAN, size, canvas)
        for ghost in self.world.ghosts:
            self.draw_entity(ghost, ghost.color, size, canvas)

    @staticmethod
    def cell_size(map: Map, canvas: Canvas) -> float:
        rows, cols = len(map), len(map[0])
        return min(canvas.winfo_width() / cols, canvas.winfo_height() / rows)

    @staticmethod
    def draw_entity(
        entity: Entity, color: str, size: float, canvas: Canvas
    ) -> None:
        x = (entity.pos.x + entity.direction.dx * entity.progress) * size
        y = (entity.pos.y + entity.direction.dy * entity.progress) * size
        canvas.create_oval(x, y, x + size, y + size, fill=color)

    @staticmethod
    def draw_map(map: Map, size: float, canvas: Canvas) -> None:
        wall_sides: dict[int, tuple[int, int, int, int]] = {
            WALL_NORTH: (0, 0, 1, 0),
            WALL_WEST: (0, 0, 0, 1),
            WALL_EAST: (1, 0, 1, 1),
            WALL_SOUTH: (0, 1, 1, 1),
        }

        for y, line in enumerate(map):
            for x, cell in enumerate(line):
                if not cell:
                    continue
                px = size * x + 1
                py = size * y + 1
                canvas.create_rectangle(
                    px, py, px + size, py + size, fill=Color.WALL, width=0
                )
                for wall, (x0, y0, x1, y1) in wall_sides.items():
                    if not cell & wall:
                        canvas.create_line(
                            px + x0 * size,
                            py + y0 * size,
                            px + x1 * size,
                            py + y1 * size,
                            fill=Color.WALL_OUTLINE,
                        )
