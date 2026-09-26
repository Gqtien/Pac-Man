from typing import Callable
from PIL.Image import Image
from config import Config
from models.world import respawn
from render import glyphs, images_size, put_images
from systems import Outcome, step
from .base import Scene, Push, Transition, Reset
from scenes.factories import SceneFactories
from .pause import Pause
from assets import (
    DOOR,
    FRAME,
    HOUSE_FRAME,
    RIM,
    Animation,
    Assets,
    FontColor,
    Frame,
    Sprites,
    Wall,
)
from models import (
    Direction,
    Entity,
    Ghost,
    GhostState,
    Pacman,
    new_map,
    new_world,
    next_level,
    is_door,
    is_house,
    is_solid, FrameBuffer,
)


class Gameplay(Scene):
    def __init__(
        self, factories: SceneFactories, config: Config, assets: Assets
    ) -> None:
        self.config = config
        self.assets = assets
        self.factories = factories
        self.world = new_world(new_map())

    def update(self, dt: float, keys: set[str]) -> Transition:
        if "Escape" in keys:
            return Push(Pause(self.config, self.assets))
        match step(self.world, self.config, dt, keys):
            case Outcome.LOST:
                score = self.world.score
                self.world = new_world(new_map())
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
                self.world = new_world(new_map())
                return Reset(
                    self.factories.win(self.config, self.assets, score)
                )
        return None

    def draw(self, framebuffer: FrameBuffer) -> None:
        framebuffer.clear(b"\x00\x00\x00\xFF")
        zoom = self.zoom(framebuffer)
        self.framebuffer = framebuffer
        self.size = 16 * zoom
        self.walls = self.assets.walls[zoom]
        sprites = self.assets.sprites[zoom]

        self.draw_map()
        self.draw_items(sprites)
        pacman = self.world.pacman
        if pacman.alive or self.world.freeze > 0:
            self.draw_entity(pacman, sprites.pacman[pacman.direction])
            for ghost in self.world.ghosts:
                self.draw_entity(ghost, self.ghost_animation(ghost, sprites))
        else:
            self.draw_death(pacman, sprites.death)
        self.draw_hud(sprites)
        self.center()

    def zoom(self, framebuffer: FrameBuffer) -> int:
        rows, cols = len(self.world.map), len(self.world.map[0])
        w, h = framebuffer.width, framebuffer.height
        return max(1, min(w // (16 * cols), h // (16 * (rows + 2))))

    def center(self) -> None:
        rows, cols = len(self.world.map), len(self.world.map[0])
        dx = (self.framebuffer.width - cols * self.size) // 2
        dy = (self.framebuffer.height - (rows + 2) * self.size) // 2
        self.framebuffer.move(dx, dy + self.size)

    @staticmethod
    def ghost_animation(ghost: Ghost, sprites: Sprites) -> Animation:
        match ghost.state:
            case (
                GhostState.CHASE
                | GhostState.SCATTER
                | GhostState.HOUSE
                | GhostState.LEAVING
            ):
                return sprites.ghost[ghost.personality][ghost.direction]
            case GhostState.DEAD:
                return [sprites.eyes[ghost.direction]]
            case GhostState.EATEN:
                return [sprites.ghost_score[ghost.value]]
            case GhostState.FRIGHTENED:
                if (
                    ghost.frightened_timer < 3
                    and int(ghost.frightened_timer * 4) % 2 == 0
                ):
                    return sprites.flashing
                return sprites.frightened

    def draw_entity(self, entity: Entity, animation: Animation) -> None:
        frame = animation[int(entity.anim_progress) % len(animation)]
        self.draw_sprite(entity, frame)

    def draw_death(self, pacman: Pacman, frames: Animation) -> None:
        index = int(pacman.death / self.config.anim_speed * len(frames))
        self.draw_sprite(pacman, frames[min(index, len(frames) - 1)])

    def draw_sprite(self, entity: Entity, frame: Image) -> None:
        x = entity.pos.x + entity.direction.dx * entity.progress + 0.5
        y = entity.pos.y + entity.direction.dy * entity.progress + 0.5
        self.framebuffer.put_image(frame, x * self.size, y * self.size)

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
        self.framebuffer.put_image(self.walls[tile], px, py)

    def cell_at(self, x: int, y: int) -> int:
        map = self.world.map
        if 0 <= y < len(map) and 0 <= x < len(map[y]):
            return map[y][x]
        return 0

    def draw_items(self, sprites: Sprites) -> None:
        for (x, y), item in self.world.items.items():
            self.framebuffer.put_image(
                sprites.items[item], x * self.size, y * self.size,
            )

    def draw_hud(self, sprites: Sprites) -> None:
        rows, cols = len(self.world.map), len(self.world.map[0])
        font = self.assets.fonts.fit(self.size / 2)[FontColor.WHITE]
        score, level = self.world.score, self.world.level
        self.put_hud(glyphs(f"Score {score}", font), 0, -1)
        self.put_hud(glyphs(f"Level {level}", font), cols, -1, right=True)
        life = sprites.pacman[Direction.EAST][1]
        self.put_hud([life] * self.world.lives, 0, rows)

    def put_hud(
        self,
        images: list[Image],
        cx: float,
        cy: float,
        right: bool = False,
    ) -> None:
        width, height = images_size(images)
        x = cx * self.size - (width if right else 0)
        y = cy * self.size + (self.size - height) / 2
        put_images(images, self.framebuffer, int(x), int(y))
