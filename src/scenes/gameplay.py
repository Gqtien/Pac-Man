from tkinter import Canvas
from typing import Callable
from config import Config
from models.world import respawn
from systems import Outcome, step
from .base import Scene
from .death import Death
from .pause import Pause
from .transition import Push, Transition
from assets import (
    DOOR,
    FRAME,
    HOUSE_FRAME,
    RIM,
    Animation,
    Assets,
    Frame,
    Sprites,
    Wall,
)
from models import (
    Direction,
    Entity,
    Ghost,
    GhostState,
    new_map,
    new_world,
    next_level,
    is_door,
    is_house,
    is_solid,
)


class Gameplay(Scene):
    def __init__(self, config: Config, assets: Assets) -> None:
        self.config = config
        self.assets = assets
        self.world = new_world(new_map())

    def update(self, dt: float, keys: set[str]) -> Transition:
        if "Escape" in keys:
            return Push(Pause(self.config, self.assets))
        match step(self.world, self.config, dt, keys):
            case Outcome.LOST:
                self.world = new_world(new_map())
                return Push(Death(self.config, self.assets))
            case Outcome.DIED:
                self.world = respawn(self.world)
            case Outcome.WON:
                self.world = next_level(self.world, new_map())
        return None

    def draw(self, canvas: Canvas) -> None:
        zoom = self.zoom(canvas)
        self.canvas = canvas
        self.size = 16 * zoom
        self.walls = self.assets.walls[zoom]
        sprites = self.assets.sprites[zoom]

        self.draw_map()
        self.draw_items(sprites)
        pacman = self.world.pacman
        self.draw_entity(pacman, sprites.pacman[pacman.direction])
        for ghost in self.world.ghosts:
            self.draw_entity(ghost, self.ghost_animation(ghost, sprites))
        self.center()

    def zoom(self, canvas: Canvas) -> int:
        rows, cols = len(self.world.map), len(self.world.map[0])
        w, h = canvas.winfo_width(), canvas.winfo_height()
        return max(1, min(w // (16 * cols), h // (16 * rows)))

    def center(self) -> None:
        rows, cols = len(self.world.map), len(self.world.map[0])
        dx = (self.canvas.winfo_width() - cols * self.size) // 2
        dy = (self.canvas.winfo_height() - rows * self.size) // 2
        self.canvas.move("all", dx, dy)

    @staticmethod
    def ghost_animation(ghost: Ghost, sprites: Sprites) -> Animation:
        match ghost.state:
            case (
                GhostState.CHASE | GhostState.SCATTER
                | GhostState.HOUSE | GhostState.LEAVING
            ):
                return sprites.ghost[ghost.personality][ghost.direction]
            case GhostState.DEAD:
                return [sprites.eyes[ghost.direction]]
            case GhostState.FRIGHTENED:
                # TODO: config
                if ghost.frightened_timer < 3 and \
                   int(ghost.frightened_timer * 4) % 2 == 0:
                    return sprites.flashing
                return sprites.frightened

    def draw_entity(self, entity: Entity, animation: Animation) -> None:
        x = entity.pos.x + entity.direction.dx * entity.progress + 0.5
        y = entity.pos.y + entity.direction.dy * entity.progress + 0.5
        frame = animation[int(entity.anim_progress) % len(animation)]
        self.canvas.create_image(x * self.size, y * self.size, image=frame)

    def draw_map(self) -> None:
        for y, line in enumerate(self.world.map):
            for x, cell in enumerate(line):
                if is_solid(cell):
                    self.draw_cell(x, y)

    def draw_cell(self, x: int, y: int) -> None:
        cell = self.world.map[y][x]
        if is_door(cell):
            side = Direction.EAST
            if is_solid(self.cell_at(x + 1, y)):
                side = Direction.WEST
            top, bottom = DOOR[side]
            self.put(top, x, y, Direction.NORTH, side)
            self.put(bottom, x, y, Direction.SOUTH, side)
        elif is_house(cell):
            self.draw_frame(x, y, HOUSE_FRAME, is_solid)
            self.draw_frame(x, y, RIM, is_house)
        else:
            self.draw_frame(x, y, FRAME, is_solid)

    def draw_frame(
        self, x: int, y: int, frame: Frame, joined: Callable[[int], bool]
    ) -> None:
        for (v, h), (corner, edge_v, edge_h, inner) in frame.items():
            side_v = joined(self.cell_at(x, y + v.dy))
            side_h = joined(self.cell_at(x + h.dx, y))
            diagonal = joined(self.cell_at(x + h.dx, y + v.dy))
            if not side_v and not side_h:
                self.put(corner, x, y, v, h)
            elif not side_v:
                self.put(edge_v, x, y, v, h)
            elif not side_h:
                self.put(edge_h, x, y, v, h)
            elif not diagonal:
                self.put(inner, x, y, v, h)

    def put(
        self, tile: Wall, x: int, y: int, v: Direction, h: Direction
    ) -> None:
        half = self.size / 2
        px = self.size * x + (half if h is Direction.EAST else 0)
        py = self.size * y + (half if v is Direction.SOUTH else 0)
        self.canvas.create_image(px, py, image=self.walls[tile], anchor="nw")

    def cell_at(self, x: int, y: int) -> int:
        map = self.world.map
        if 0 <= y < len(map) and 0 <= x < len(map[y]):
            return map[y][x]
        return 0

    def draw_items(self, sprites: Sprites) -> None:
        for (x, y), item in self.world.items.items():
            self.canvas.create_image(
                x * self.size,
                y * self.size,
                image=sprites.items[item],
                anchor="nw",
            )
