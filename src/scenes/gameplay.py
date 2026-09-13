from tkinter import Canvas
from models import Transition, Pacman, World
from models.utils import WALL_NORTH, WALL_EAST, WALL_SOUTH, WALL_WEST, Vec2
from .base import Scene
from models.utils import maze_to_grid, grid_to_walls
from mazegenerator import MazeGenerator


class Gameplay(Scene):
    def __init__(self) -> None:
        self.world: World = World(
            grid_to_walls(maze_to_grid(MazeGenerator().maze)),
            Pacman(pos=Vec2(1, 1), direction=Vec2(0, 0)),
            [],
            0
        )
        self.input_buffer: list[str] = []

    def update(self, dt: float, keys: set[str]) -> Transition:
        self.input_buffer.extend(list(keys))
        self.update_pacman(self.world.pacman, dt, keys)

    def draw(self, canvas: Canvas) -> None:
        cell_size: float = self.get_cell_size(canvas)
        self.draw_background(self.world.map, cell_size, canvas)
        self.draw_map(self.world.map, cell_size, canvas)
        self.draw_pacman(self.world.pacman, cell_size, canvas)

    @staticmethod
    def draw_pacman(pacman: Pacman, cell_size: float, canvas: Canvas) -> None:
        # Scale position from map coords to pixel coords.
        x = pacman.pos.x + pacman.direction.x * pacman.movement_progress + 0.5
        y = pacman.pos.y + pacman.direction.y * pacman.movement_progress + 0.5
        x *= cell_size
        y *= cell_size
        canvas.create_oval(
            x - cell_size / 2, y - cell_size / 2,
            x + cell_size / 2, y + cell_size / 2,
            fill="Yellow"
        )

    def update_pacman(self, pacman: Pacman, dt: float, keys: set[str]) -> None:
        # Move along direction.
        # TODO: speed in config
        pacman.movement_progress += 3 * dt

        if pacman.movement_progress < 1.0:
            return

        # reset move
        pacman.movement_progress = 0.0
        pacman.pos.x += pacman.direction.x
        pacman.pos.y += pacman.direction.y

        # update direction
        direction = Vec2(0, 0)
        # Read input buffer.
        while self.input_buffer:
            key: str = self.input_buffer.pop(0)
            match key:
                case "Up":
                    direction.update(0, -1)
                case "Down":
                    direction.update(0, 1)
                case "Left":
                    direction.update(-1, 0)
                case "Right":
                    direction.update(1, 0)
            if direction != Vec2(0, 0):
                # try to move to the last input
                if self.can_move(pacman.pos, direction):
                    pacman.direction = direction
                    return
                # only consume first input in the buffer
                break
        # try to move to the old direction
        if not self.can_move(pacman.pos, pacman.direction):
            pacman.direction.update(0, 0)

    def can_move(
            self, pos: Vec2, direction: Vec2
    ) -> bool:
        """Check if there is a wall in this direction."""
        x = int(pos.x + direction.x)
        y = int(pos.y + direction.y)
        if x < 0 or y < 0:
            return False
        if x >= len(self.world.map[0]) or y >= len(self.world.map):
            return False
        if self.world.map[y][x]:
            return False
        return True

    def get_cell_size(self, canvas: Canvas) -> float:
        cell_size: float = 0
        if len(self.world.map):
            cell_size = canvas.winfo_height() / len(self.world.map)
        if len(self.world.map[0]):
            if (size := canvas.winfo_width() / len(self.world.map[0])) < cell_size:
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

    @staticmethod
    def draw_background(map: list[list[int]], size: float, canvas: Canvas) -> None:
        for y, line in enumerate(map):
            for x, cell in enumerate(line):
                if cell:
                    continue
                px = size * x + 1
                py = size * y + 1
                canvas.create_rectangle(
                    px, py, px + size, py + size, fill="black", width=0
                )
