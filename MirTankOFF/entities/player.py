# entities/player.py
import pygame

from settings import *
from entities.bullet import Bullet
from core.sprites import blit_tank
from core.grid_movement import GridGlideMovement

MOVE_KEYS = (
    (pygame.K_w, pygame.K_UP, 1094, 1062, "up"),
    (pygame.K_s, pygame.K_DOWN, 1099, 1067, "down"),
    (pygame.K_a, pygame.K_LEFT, 1092, 1060, "left"),
    (pygame.K_d, pygame.K_RIGHT, 1074, 1042, "right"),
)


class Player(GridGlideMovement):
    def __init__(self, x, y):
        self._init_grid_glide(x, y)
        self.size = TANK_SIZE
        self.dir = "up"

        self.max_hp = get_player_max_hp()
        self.hp = self.max_hp
        self.coins = 0
        self.score = 0

        self.cooldown = 0
        self.i_frames = 0
        self.interact_cooldown = 0

        try:
            img = pygame.image.load(asset_path("танк.png")).convert_alpha()
            self.original_image = img
        except FileNotFoundError:
            self.original_image = None

    def _read_move_direction(self, keys):
        for key_codes in MOVE_KEYS:
            if any(keys[k] for k in key_codes[:-1]):
                return key_codes[-1]
        return None

    def interact(self, dungeon, audio=None):
        if self.interact_cooldown > 0:
            return
        if dungeon.doors_locked:
            return

        player_rect = pygame.Rect(self.render_x, self.render_y + ARENA_Y, self.size, self.size)
        interaction_zone = player_rect.inflate(8, 8)
        heal_cost = get_heal_cost()

        for shop_rect in dungeon.get_shop_rects():
            if interaction_zone.colliderect(shop_rect):
                if self.coins >= heal_cost and self.hp < self.max_hp:
                    self.coins -= heal_cost
                    self.hp += 1
                    self.interact_cooldown = 30
                    dungeon.mark_shop_opened()
                    if audio is not None:
                        audio.play("heal")
                break

    def _should_block_door_exit(self, dungeon, direction):
        """Не даёт съехать с двери до срабатывания перехода."""
        passage = dungeon.get_passage_at(self.grid_col(), self.grid_row())
        if not passage:
            return False
        inward = {"top": "down", "bottom": "up", "left": "right", "right": "left"}
        return direction == inward.get(passage)

    def _glide_speed(self, dungeon):
        speed = float(GLIDE_PIXELS_PER_FRAME)
        if dungeon.is_in_bush(self.render_x, self.render_y, self.size):
            speed *= BUSH_SLOWDOWN_MULTIPLIER
        return speed

    def update(self, keys, dungeon, bullets, enemies, audio=None):
        if self.cooldown > 0:
            self.cooldown -= 1
        if self.i_frames > 0:
            self.i_frames -= 1
        if self.interact_cooldown > 0:
            self.interact_cooldown -= 1

        self._update_glide(self._glide_speed(dungeon))

        self.tick_cooldowns()

        direction = self._read_move_direction(keys)
        if direction and not self._should_block_door_exit(dungeon, direction):
            self.try_grid_move(direction, self.size, dungeon, enemies)

        if keys[pygame.K_SPACE] and self.cooldown == 0:
            bullets.append(Bullet.from_tank(self.x, self.y, self.size, self.dir, is_player=True))
            self.cooldown = PLAYER_SHOOT_COOLDOWN
            if audio is not None:
                audio.play("shoot")

        if keys[pygame.K_e] or keys[1091] or keys[1059]:
            self.interact(dungeon, audio=audio)

    def draw(self, screen):
        if self.i_frames > 0 and (self.i_frames // 6) % 2 == 0:
            return

        draw_y = self.render_y + ARENA_Y
        if self.original_image:
            blit_tank(screen, self.original_image, self.render_x, draw_y, self.size, self.dir)
        else:
            self._draw_placeholder(screen, draw_y)

    def _draw_placeholder(self, screen, draw_y):
        x = int(self.render_x)
        body_color = PLAYER_COLOR
        track_color = (40, 40, 40)

        if self.dir in ("up", "down"):
            pygame.draw.rect(screen, track_color, (x, draw_y, 4, self.size))
            pygame.draw.rect(screen, track_color, (x + self.size - 4, draw_y, 4, self.size))
            pygame.draw.rect(screen, body_color, (x + 4, draw_y + 2, self.size - 8, self.size - 4))
        else:
            pygame.draw.rect(screen, track_color, (x, draw_y, self.size, 4))
            pygame.draw.rect(screen, track_color, (x, draw_y + self.size - 4, self.size, 4))
            pygame.draw.rect(screen, body_color, (x + 2, draw_y + 4, self.size - 4, self.size - 8))