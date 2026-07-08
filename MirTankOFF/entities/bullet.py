# entities/bullet.py
import pygame

from settings import *

_bullet_sprites = {}


def muzzle_position(x, y, size, direction):
    """Точка выстрела у дула (спрайт по умолчанию смотрит вниз)."""
    cx = x + size // 2
    cy = y + size // 2
    offset = size // 2 + 2

    if direction == "down":
        return cx, cy + offset
    if direction == "up":
        return cx, cy - offset
    if direction == "left":
        return cx - offset, cy
    return cx + offset, cy


def _load_bullet_sprite(is_player):
    if is_player in _bullet_sprites:
        return _bullet_sprites[is_player]

    filename = "выстрел гг.png" if is_player else "вражеский выстрел.png"
    try:
        img = pygame.image.load(asset_path(filename)).convert_alpha()
    except FileNotFoundError:
        img = None
    _bullet_sprites[is_player] = img
    return img


class Bullet:
    def __init__(self, x, y, direction, is_player):
        self.x = x
        self.y = y
        self.dir = direction
        self.is_player = is_player
        self.speed = BULLET_SPEED
        self.radius = BULLET_RADIUS_PLAYER if is_player else BULLET_RADIUS_ENEMY
        self.active = True
        self.sprite = _load_bullet_sprite(is_player)

    @classmethod
    def from_tank(cls, x, y, size, direction, is_player):
        bx, by = muzzle_position(x, y, size, direction)
        return cls(bx, by, direction, is_player)

    def update(self, dungeon):
        if self.dir == "up":
            self.y -= self.speed
        elif self.dir == "down":
            self.y += self.speed
        elif self.dir == "left":
            self.x -= self.speed
        elif self.dir == "right":
            self.x += self.speed

        col = int(self.x // TILE_SIZE)
        row = int(self.y // TILE_SIZE)
        matrix = dungeon.get_matrix()

        if 0 <= row < ROWS and 0 <= col < COLS:
            tile = matrix[row][col]

            if tile == TILE_OBSTACLE:
                matrix[row][col] = TILE_EMPTY
                self.active = False
            elif tile in (TILE_WALL, TILE_SHOP):
                self.active = False
            elif tile == TILE_DOOR and dungeon.doors_locked:
                self.active = False
        else:
            self.active = False

    def draw(self, screen):
        draw_y = self.y + ARENA_Y
        if self.sprite:
            rect = self.sprite.get_rect(center=(int(self.x), int(draw_y)))
            screen.blit(self.sprite, rect)
        else:
            if self.is_player:
                outer_color = (200, 150, 0)
                inner_color = (255, 255, 0)
            else:
                outer_color = (150, 0, 0)
                inner_color = (255, 0, 0)
            pygame.draw.circle(screen, outer_color, (int(self.x), int(draw_y)), self.radius + 2)
            pygame.draw.circle(screen, inner_color, (int(self.x), int(draw_y)), self.radius)
