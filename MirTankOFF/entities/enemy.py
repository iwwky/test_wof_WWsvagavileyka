# entities/enemy.py
import pygame
import random

from settings import *
from entities.bullet import Bullet
from core.sprites import blit_tank
from core.grid_movement import GridGlideMovement


class Coin:
    """Монетка, выпадающая из врагов."""

    _sprite = None
    _sprite_loaded = False

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 5
        self.float_offset = 0.0
        self.float_dir = 0.15

        if not Coin._sprite_loaded:
            Coin._sprite_loaded = True
            try:
                img = pygame.image.load(asset_path("монета.png")).convert_alpha()
                Coin._sprite = pygame.transform.scale(img, (14, 14))
            except FileNotFoundError:
                Coin._sprite = None

    def update(self):
        self.float_offset += self.float_dir
        if self.float_offset > 2 or self.float_offset < -2:
            self.float_dir *= -1

    def draw(self, screen):
        draw_y = self.y + self.float_offset + ARENA_Y
        if Coin._sprite:
            rect = Coin._sprite.get_rect(center=(int(self.x), int(draw_y)))
            screen.blit(Coin._sprite, rect)
        else:
            pygame.draw.circle(screen, COIN_COLOR, (int(self.x), int(draw_y)), self.radius)
            pygame.draw.circle(screen, (200, 150, 0), (int(self.x), int(draw_y)), self.radius - 2)


class Enemy(GridGlideMovement):
    def __init__(self, x, y, is_boss=False):
        self._init_grid_glide(x, y)
        self.is_boss = is_boss

        diff = get_difficulty_settings()
        self.size = BOSS_SIZE if is_boss else TANK_SIZE
        self.hp = diff["boss_hp"] if is_boss else diff["enemy_hp"]
        self.max_hp = self.hp
        self.speed_mult = 1.0 if is_boss else diff["enemy_speed_mult"]
        self.fire_chance = diff["boss_fire_chance"] if is_boss else diff["enemy_fire_chance"]

        self.dir = "down"
        self.cooldown = 0
        self.move_timer = 0
        self.shoot_cooldown = diff["boss_shoot_cooldown"] if is_boss else ENEMY_SHOOT_COOLDOWN

        self.original_image = None
        sprite_file = "босс.png" if is_boss else "танк(враг).png"

        try:
            img = pygame.image.load(asset_path(sprite_file)).convert_alpha()
            self.original_image = pygame.transform.scale(img, (self.size, self.size))
        except FileNotFoundError:
            if is_boss:
                try:
                    img = pygame.image.load(asset_path("танк(враг).png")).convert_alpha()
                    self.original_image = pygame.transform.scale(img, (self.size, self.size))
                except FileNotFoundError:
                    pass

    def _movement_blockers(self, player, enemies):
        blockers = [player]
        for other in enemies:
            if other is not self:
                blockers.append(other)
        return blockers

    def _glide_speed(self, dungeon):
        speed = GLIDE_PIXELS_PER_FRAME * self.speed_mult
        if dungeon.is_in_bush(self.render_x, self.render_y, self.size):
            speed *= BUSH_SLOWDOWN_MULTIPLIER
        return speed

    def update(self, dungeon, bullets, player, enemies):
        if self.cooldown > 0:
            self.cooldown -= 1
        if self.move_timer > 0:
            self.move_timer -= 1

        self._update_glide(self._glide_speed(dungeon))

        if not self.is_gliding:
            if self.move_timer <= 0:
                self.dir = random.choice(["up", "down", "left", "right"])
                self.move_timer = random.randint(60, 120) if self.is_boss else random.randint(30, 90)

            blockers = self._movement_blockers(player, enemies)
            if not self.try_grid_move(self.dir, self.size, dungeon, blockers):
                self.dir = random.choice(["up", "down", "left", "right"])
                self.move_timer = random.randint(20, 60)
                self.try_grid_move(self.dir, self.size, dungeon, blockers)

        if random.random() < self.fire_chance and self.cooldown == 0:
            if self.is_boss:
                for d in ("up", "down", "left", "right"):
                    bullets.append(Bullet.from_tank(self.x, self.y, self.size, d, is_player=False))
                self.cooldown = self.shoot_cooldown
            else:
                bullets.append(Bullet.from_tank(self.x, self.y, self.size, self.dir, is_player=False))
                self.cooldown = self.shoot_cooldown

    def get_loot(self):
        loot = []
        drop_count = BOSS_COIN_DROP if self.is_boss else (1 if random.random() < COIN_DROP_CHANCE else 0)

        for _ in range(drop_count):
            offset_x = random.randint(-12, 12)
            offset_y = random.randint(-12, 12)
            coin_x = self.x + self.size // 2 + offset_x
            coin_y = self.y + self.size // 2 + offset_y
            coin_x = max(TILE_SIZE, min(coin_x, WIDTH - TILE_SIZE))
            coin_y = max(TILE_SIZE, min(coin_y, ARENA_HEIGHT - TILE_SIZE))
            loot.append(Coin(coin_x, coin_y))

        return loot

    def draw(self, screen):
        draw_y = self.render_y + ARENA_Y
        x = int(self.render_x)

        if self.original_image:
            blit_tank(screen, self.original_image, self.render_x, draw_y, self.size, self.dir)
        else:
            body_color = BOSS_COLOR if self.is_boss else ENEMY_COLOR
            pygame.draw.rect(screen, body_color, (x, draw_y, self.size, self.size))

        if self.is_boss:
            hp_ratio = max(0, self.hp) / self.max_hp
            pygame.draw.rect(screen, (50, 50, 50), (x, draw_y - 6, self.size, 4))
            pygame.draw.rect(screen, (255, 50, 50), (x, draw_y - 6, int(self.size * hp_ratio), 4))
            pygame.draw.rect(screen, COIN_COLOR, (x, draw_y - 6, self.size, 4), 1)