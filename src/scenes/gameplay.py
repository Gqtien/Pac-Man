from tkinter import Canvas
import systems
from systems import Outcome
from models import Direction, Ghost, Pacman, Personality, World
from models.vec import Vec2
from utils import (
    WALL_NORTH,
    WALL_EAST,
    WALL_SOUTH,
    WALL_WEST,
    maze_to_grid,
    grid_to_walls,
)
from mazegenerator import MazeGenerator
from .base import Scene
from .death import Death
from .main import Main
from .transition import Push, Reset, Transition


class Gameplay(Scene):
    def __init__(self) -> None:
        # TODO: figure out start pos of pacman and ghosts
        self.world: World = World(
            grid_to_walls(maze_to_grid(MazeGenerator().maze)),
            Pacman(pos=Vec2(1, 1), direction=Direction.NONE),
            [
                Ghost(Vec2(11, 1), Direction.NONE, Personality.BLINKY),
            ],
        )

    def update(self, dt: float, keys: set[str]) -> Transition:
        match systems.step(self.world, dt, keys):
            case Outcome.LOST:
                return Push(Death())
            case Outcome.WON:
                return Reset(Main())
            case _:
                return None

    def draw(self, canvas: Canvas) -> None:
        cell_size: float = self.get_cell_size(canvas)
        canvas.delete("all")
        self.draw_map(self.world.map, cell_size, canvas)
        self.draw_pacman(self.world.pacman, cell_size, canvas)
        for ghost in self.world.ghosts:
            self.draw_ghost(ghost, cell_size, canvas)

    @staticmethod
    def draw_pacman(pacman: Pacman, cell_size: float, canvas: Canvas) -> None:
        # Scale position from map coords to pixel coords.
        x = pacman.pos.x + pacman.direction.dx * pacman.progress
        y = pacman.pos.y + pacman.direction.dy * pacman.progress
        x *= cell_size
        y *= cell_size
        canvas.create_oval(x, y, x + cell_size, y + cell_size, fill="Yellow")

    @staticmethod
    def draw_ghost(ghost: Ghost, cell_size: float, canvas: Canvas) -> None:
        # Scale position from map coords to pixel coords.
        x = ghost.pos.x + ghost.direction.dx * ghost.progress
        y = ghost.pos.y + ghost.direction.dy * ghost.progress
        x *= cell_size
        y *= cell_size
        canvas.create_oval(
            x,
            y,
            x + cell_size,
            y + cell_size,
            fill=ghost.personality.value.value,
        )

    def get_cell_size(self, canvas: Canvas) -> float:
        cell_size: float = 0
        if len(self.world.map):
            cell_size = canvas.winfo_height() / len(self.world.map)
        if len(self.world.map[0]):
            if (
                size := canvas.winfo_width() / len(self.world.map[0])
            ) < cell_size:
                cell_size = size
        return cell_size

    @staticmethod
    def draw_map(map: list[list[int]], size: float, canvas: Canvas) -> None:
        for y, line in enumerate(map):
            for x, cell in enumerate(line):
                if not cell:
                    continue
                px = size * x + 1
                py = size * y + 1
                canvas.create_rectangle(
                    px, py, px + size, py + size, fill="darkblue", width=0
                )
                if cell & WALL_NORTH == 0:
                    canvas.create_line(px, py, px + size, py, fill="blue")
                if cell & WALL_WEST == 0:
                    canvas.create_line(px, py, px, py + size, fill="blue")
                if cell & WALL_EAST == 0:
                    canvas.create_line(
                        px + size, py, px + size, py + size, fill="blue"
                    )
                if cell & WALL_SOUTH == 0:
                    canvas.create_line(
                        px, py + size, px + size, py + size, fill="blue"
                    )
