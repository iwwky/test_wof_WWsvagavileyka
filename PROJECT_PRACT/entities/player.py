# entities/player.py
import pygame
from settings import *
from entities.bullet import Bullet
from core.sprites import blit_tank


MOVE_KEYS = (
    (pygame.K_w, pygame.K_UP, 1094, 1062, "up"),
    (pygame.K_s, pygame.K_DOWN, 1099, 1067, "down"),
    (pygame.K_a, pygame.K_LEFT, 1092, 1060, "left"),
    (pygame.K_d, pygame.K_RIGHT, 1074, 1042, "right"),
)


class Player:
    def __init__(self, x, y):
        self.x = self._snap(x)
        self.y = self._snap(y)
        self.size = TANK_SIZE
        self.dir = "up"

        self.hp = PLAYER_MAX_HP
        self.score = 0

        self.cooldown = 0
        self.i_frames = 0
        self.interact_cooldown = 0
        self.grid_move_cooldown = 0

        try:
            img = pygame.image.load(asset_path("танк.png")).convert_alpha()
            self.original_image = img
        except FileNotFoundError:
            self.original_image = None
            print("ВНИМАНИЕ: Спрайт 'танк.png' не найден. Включена заглушка.")

    @staticmethod
    def _snap(value):
        return (value // TILE_SIZE) * TILE_SIZE

    def grid_col(self):
        return self.x // TILE_SIZE

    def grid_row(self):
        return self.y // TILE_SIZE

    def _read_move_direction(self, keys):
        for key_codes in MOVE_KEYS:
            if any(keys[k] for k in key_codes[:-1]):
                return key_codes[-1]
        return None

    def try_grid_move(self, direction, dungeon, enemies):
        """Move exactly one tile (16 px); position stays grid-aligned."""
        self.dir = direction

        dx, dy = 0, 0
        if direction == "up":
            dy = -TILE_SIZE
        elif direction == "down":
            dy = TILE_SIZE
        elif direction == "left":
            dx = -TILE_SIZE
        elif direction == "right":
            dx = TILE_SIZE

        new_x = self.x + dx
        new_y = self.y + dy

        if new_x < 0 or new_y < 0 or new_x > WIDTH - self.size or new_y > ARENA_HEIGHT - self.size:
            return False

        if dungeon.check_collision(new_x, new_y, self.size):
            return False

        player_rect = pygame.Rect(new_x, new_y, self.size, self.size)
        for enemy in enemies:
            if player_rect.colliderect(pygame.Rect(enemy.x, enemy.y, enemy.size, enemy.size)):
                return False

        self.x = new_x
        self.y = new_y
        return True

    def interact(self, dungeon):
        if self.interact_cooldown > 0:
            return

        player_rect = pygame.Rect(self.x, self.y + ARENA_Y, self.size, self.size)
        interaction_zone = player_rect.inflate(8, 8)

        for shop_rect in dungeon.get_shop_rects():
            if interaction_zone.colliderect(shop_rect):
                if self.hp < PLAYER_MAX_HP:
                    self.hp += 1
                    self.interact_cooldown = 30
                break

    def update(self, keys, dungeon, bullets, enemies):
        if self.cooldown > 0:
            self.cooldown -= 1
        if self.i_frames > 0:
            self.i_frames -= 1
        if self.interact_cooldown > 0:
            self.interact_cooldown -= 1

        direction = self._read_move_direction(keys)
        if direction:
            if self.grid_move_cooldown <= 0:
                self.try_grid_move(direction, dungeon, enemies)
                self.grid_move_cooldown = GRID_MOVE_DELAY
            else:
                self.grid_move_cooldown -= 1
        else:
            self.grid_move_cooldown = 0

        if keys[pygame.K_SPACE] and self.cooldown == 0:
            bullets.append(Bullet.from_tank(self.x, self.y, self.size, self.dir, is_player=True))
            self.cooldown = PLAYER_SHOOT_COOLDOWN

        if keys[pygame.K_e] or keys[1091] or keys[1059]:
            self.interact(dungeon)

    def draw(self, screen):
        if self.i_frames > 0 and (self.i_frames // 6) % 2 == 0:
            return

        draw_y = self.y + ARENA_Y
        if self.original_image:
            blit_tank(screen, self.original_image, self.x, draw_y, self.size, self.dir)
        else:
            self._draw_placeholder(screen, draw_y)

    def _draw_placeholder(self, screen, draw_y):
        body_color = PLAYER_COLOR
        track_color = (40, 40, 40)

        if self.dir in ("up", "down"):
            pygame.draw.rect(screen, track_color, (self.x, draw_y, 4, self.size))
            pygame.draw.rect(screen, track_color, (self.x + self.size - 4, draw_y, 4, self.size))
            pygame.draw.rect(screen, body_color, (self.x + 4, draw_y + 2, self.size - 8, self.size - 4))
        else:
            pygame.draw.rect(screen, track_color, (self.x, draw_y, self.size, 4))
            pygame.draw.rect(screen, track_color, (self.x, draw_y + self.size - 4, self.size, 4))
            pygame.draw.rect(screen, body_color, (self.x + 2, draw_y + 4, self.size - 4, self.size - 8))
