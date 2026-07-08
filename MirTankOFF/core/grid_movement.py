# core/grid_movement.py
"""Логическая сетка + плавная интерполяция между клетками."""
import pygame

from settings import TILE_SIZE, GLIDE_PIXELS_PER_FRAME, WIDTH, ARENA_HEIGHT


class GridGlideMovement:
    def _init_grid_glide(self, x, y):
        self.x = self._snap(x)
        self.y = self._snap(y)
        self.render_x = float(self.x)
        self.render_y = float(self.y)
        self.is_gliding = False
        self._glide_target_x = self.x
        self._glide_target_y = self.y
        self.transition_cooldown = 0

    @staticmethod
    def _snap(value):
        return (value // TILE_SIZE) * TILE_SIZE

    def grid_col(self):
        return self.x // TILE_SIZE

    def grid_row(self):
        return self.y // TILE_SIZE

    def teleport(self, x, y):
        """Мгновенная установка позиции (переход через дверь)."""
        self.x = self._snap(x)
        self.y = self._snap(y)
        self.render_x = float(self.x)
        self.render_y = float(self.y)
        self.is_gliding = False
        self._glide_target_x = self.x
        self._glide_target_y = self.y

    def _direction_delta(self, direction):
        if direction == "up":
            return 0, -TILE_SIZE
        if direction == "down":
            return 0, TILE_SIZE
        if direction == "left":
            return -TILE_SIZE, 0
        return TILE_SIZE, 0

    def _update_glide(self, speed=None):
        if not self.is_gliding:
            return

        glide_speed = GLIDE_PIXELS_PER_FRAME if speed is None else speed

        tx = float(self._glide_target_x)
        ty = float(self._glide_target_y)
        dx, dy = tx - self.render_x, ty - self.render_y
        dist = (dx * dx + dy * dy) ** 0.5

        if dist <= glide_speed:
            self.render_x, self.render_y = tx, ty
            self.x = int(tx)
            self.y = int(ty)
            self.is_gliding = False
        else:
            step = glide_speed / dist
            self.render_x += dx * step
            self.render_y += dy * step

    def _begin_glide(self, new_x, new_y):
        self._glide_target_x = new_x
        self._glide_target_y = new_y
        self.is_gliding = True

    @staticmethod
    def _footprint_cells(x, y, size):
        start_col = x // TILE_SIZE
        end_col = (x + size - 1) // TILE_SIZE
        start_row = y // TILE_SIZE
        end_row = (y + size - 1) // TILE_SIZE
        return {(row, col) for row in range(start_row, end_row + 1) for col in range(start_col, end_col + 1)}

    def _entity_cells(self, entity):
        cells = self._footprint_cells(entity.x, entity.y, entity.size)
        if entity.is_gliding:
            cells |= self._footprint_cells(
                entity._glide_target_x,
                entity._glide_target_y,
                entity.size,
            )
        return cells

    def _can_occupy(self, new_x, new_y, size, dungeon, blockers):
        if new_x < 0 or new_y < 0 or new_x + size > WIDTH or new_y + size > ARENA_HEIGHT:
            return False

        if dungeon.check_collision(new_x, new_y, size):
            return False

        my_target = self._footprint_cells(new_x, new_y, size)
        for other in blockers:
            if other is self:
                continue
            if my_target & self._entity_cells(other):
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

    def tick_cooldowns(self):
        if self.transition_cooldown > 0:
            self.transition_cooldown -= 1
