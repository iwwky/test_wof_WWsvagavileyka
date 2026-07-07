# core/grid_movement.py
"""Logical grid position + smooth visual interpolation between tiles."""
import pygame
from settings import TILE_SIZE, GLIDE_PIXELS_PER_FRAME, WIDTH, ARENA_HEIGHT


class GridGlideMovement:
    def _init_grid_glide(self, x, y):
        self.x = self._snap(x)
        self.y = self._snap(y)
        self.render_x = float(self.x)
        self.render_y = float(self.y)
        self.is_gliding = False
        self._glide_target = (float(self.x), float(self.y))

    @staticmethod
    def _snap(value):
        return (value // TILE_SIZE) * TILE_SIZE

    def grid_col(self):
        return self.x // TILE_SIZE

    def grid_row(self):
        return self.y // TILE_SIZE

    def _direction_delta(self, direction):
        if direction == "up":
            return 0, -TILE_SIZE
        if direction == "down":
            return 0, TILE_SIZE
        if direction == "left":
            return -TILE_SIZE, 0
        return TILE_SIZE, 0

    def _update_glide(self):
        if not self.is_gliding:
            return

        tx, ty = self._glide_target
        dx, dy = tx - self.render_x, ty - self.render_y
        dist = (dx * dx + dy * dy) ** 0.5

        if dist <= GLIDE_PIXELS_PER_FRAME:
            self.render_x, self.render_y = tx, ty
            self.is_gliding = False
        else:
            step = GLIDE_PIXELS_PER_FRAME / dist
            self.render_x += dx * step
            self.render_y += dy * step

    def _begin_glide(self, new_x, new_y):
        self.x = new_x
        self.y = new_y
        self._glide_target = (float(new_x), float(new_y))
        self.is_gliding = True

    def _can_occupy(self, new_x, new_y, size, dungeon, blockers):
        if new_x < 0 or new_y < 0 or new_x > WIDTH - size or new_y > ARENA_HEIGHT - size:
            return False
        if dungeon.check_collision(new_x, new_y, size):
            return False

        rect = pygame.Rect(new_x, new_y, size, size)
        for other in blockers:
            other_rect = pygame.Rect(other.x, other.y, other.size, other.size)
            if rect.colliderect(other_rect):
                return False
        return True

    def try_grid_move(self, direction, size, dungeon, blockers):
        if self.is_gliding:
            return False

        self.dir = direction
        dx, dy = self._direction_delta(direction)
        new_x, new_y = self.x + dx, self.y + dy

        if not self._can_occupy(new_x, new_y, size, dungeon, blockers):
            return False

        self._begin_glide(new_x, new_y)
        return True
