from tkinter import Canvas
from models import Transition
from models.utils import WALL_NORTH, WALL_EAST, WALL_SOUTH, WALL_WEST
from .base import Scene
from models.utils import maze_to_grid, grid_to_walls
from mazegenerator import MazeGenerator


class Gameplay(Scene):
    def __init__(self) -> None:
        self.maze: list[list[int]] = grid_to_walls(maze_to_grid(
            MazeGenerator().maze)
        )

    def update(self, dt: float, keys: set[str]) -> Transition:
        pass

    def draw(self, canvas: Canvas) -> None:
        # clear bg
        canvas.create_rectangle(
            0, 0, canvas.winfo_width(), canvas.winfo_height(),
            fill="black"
        )

        cell_size: float = self.get_cell_size(canvas)
        self.draw_maze(cell_size, canvas)

    def get_cell_size(self, canvas: Canvas) -> float:
        cell_size: float = 0
        if len(self.maze):
            cell_size = canvas.winfo_height() / len(self.maze)
        if len(self.maze[0]):
            if (size := canvas.winfo_width() / len(self.maze[0])) < cell_size:
                cell_size = size
        return cell_size


    def draw_maze(self, size: float, canvas: Canvas) -> None:
        for y, line in enumerate(self.maze):
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
