from tkinter import Canvas
from .transition import Transition
from models import Pacman, World, Ghost, Personality
from utils import WALL_NORTH, WALL_EAST, WALL_SOUTH, WALL_WEST
from models.vec import Vec2
from .base import Scene
from utils import maze_to_grid, grid_to_walls
from mazegenerator import MazeGenerator


class Gameplay(Scene):
    def __init__(self) -> None:
        # TODO: figure out start pos of pacman and ghosts
        self.world: World = World(
            grid_to_walls(maze_to_grid(MazeGenerator().maze)),
            Pacman(pos=Vec2(1, 1), direction=Vec2(0, 0)),
            [
                Ghost(Vec2(11, 1), Vec2(0, 0), Personality.BLINKY),
            ],
        )
        self.input_buffer: list[str] = []

    def update(self, dt: float, keys: set[str]) -> Transition:
        self.input_buffer.extend(list(keys))
        self.update_pacman(
            self.world.pacman, dt, self.input_buffer, self.world.map
        )
        return None

    def draw(self, canvas: Canvas) -> None:
        cell_size: float = self.get_cell_size(canvas)
        canvas.delete("all")
        self.draw_map(self.world.map, cell_size, canvas)
        for ghost in self.world.ghosts:
            self.draw_ghost(ghost, cell_size, canvas)
        self.draw_pacman(self.world.pacman, cell_size, canvas)

    @staticmethod
    def draw_pacman(pacman: Pacman, cell_size: float, canvas: Canvas) -> None:
        # Scale position from map coords to pixel coords.
        x = pacman.pos.x + pacman.direction.x * pacman.movement_progress
        y = pacman.pos.y + pacman.direction.y * pacman.movement_progress
        x *= cell_size
        y *= cell_size
        canvas.create_oval(x, y, x + cell_size, y + cell_size, fill="Yellow")

    @staticmethod
    def draw_ghost(ghost: Ghost, cell_size: float, canvas: Canvas) -> None:
        # Scale position from map coords to pixel coords.
        x = ghost.pos.x + ghost.direction.x * ghost.movement_progress
        y = ghost.pos.y + ghost.direction.y * ghost.movement_progress
        x *= cell_size
        y *= cell_size
        canvas.create_oval(
            x, y, x + cell_size, y + cell_size,
            fill=ghost.personality.value.value
        )

    @staticmethod
    def update_pacman(
            pacman: Pacman,
            dt: float,
            input_buffer: list[str],
            map: list[list[int]]
    ) -> None:
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
        while input_buffer:
            key: str = input_buffer.pop(0)
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
                if Gameplay.can_move(pacman.pos, direction, map):
                    pacman.direction = direction
                    return
                # only consume first input in the buffer
                break
        # try to move to the old direction
        if not Gameplay.can_move(pacman.pos, pacman.direction, map):
            pacman.direction.update(0, 0)

    @staticmethod
    def can_move(
            pos: Vec2, direction: Vec2, map: list[list[int]]
    ) -> bool:
        """Check if there is a wall in this direction."""
        x = int(pos.x + direction.x)
        y = int(pos.y + direction.y)
        if x < 0 or y < 0:
            return False
        if x >= len(map[0]) or y >= len(map):
            return False
        if map[y][x]:
            return False
        return True

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
