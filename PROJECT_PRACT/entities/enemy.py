# entities/enemy.py
import pygame
import random
from settings import *
from entities.bullet import Bullet
from core.sprites import blit_tank
from core.grid_movement import GridGlideMovement


class Enemy(GridGlideMovement):
    def __init__(self, x, y, is_boss=False):
        self._init_grid_glide(x, y)
        self.is_boss = is_boss

        self.size = BOSS_SIZE if is_boss else TANK_SIZE
        self.hp = BOSS_HP if is_boss else ENEMY_HP

        self.dir = "down"
        self.cooldown = 0
        self.move_timer = 0

        self.original_image = None
        sprite_file = "танк(враг).png"

        try:
            img = pygame.image.load(asset_path(sprite_file)).convert_alpha()
            if is_boss:
                self.original_image = pygame.transform.scale(img, (self.size, self.size))
            else:
                self.original_image = img
        except FileNotFoundError:
            print(f"ВНИМАНИЕ: Спрайт '{sprite_file}' не найден. Включена заглушка.")

    def _movement_blockers(self, player, enemies):
        blockers = [player]
        for other in enemies:
            if other is not self:
                blockers.append(other)
        return blockers

    def update(self, dungeon, bullets, player, enemies):
        if self.cooldown > 0:
            self.cooldown -= 1
        if self.move_timer > 0:
            self.move_timer -= 1

        self._update_glide()

        if not self.is_gliding:
            if self.move_timer <= 0:
                self.dir = random.choice(["up", "down", "left", "right"])
                self.move_timer = random.randint(60, 120) if self.is_boss else random.randint(30, 90)

            blockers = self._movement_blockers(player, enemies)
            if not self.try_grid_move(self.dir, self.size, dungeon, blockers):
                self.dir = random.choice(["up", "down", "left", "right"])
                self.move_timer = random.randint(20, 60)
                self.try_grid_move(self.dir, self.size, dungeon, blockers)

        fire_chance = BOSS_FIRE_CHANCE if self.is_boss else ENEMY_FIRE_CHANCE
        if random.random() < fire_chance and self.cooldown == 0:
            if self.is_boss:
                for d in ("up", "down", "left", "right"):
                    bullets.append(Bullet.from_tank(self.x, self.y, self.size, d, is_player=False))
                self.cooldown = BOSS_SHOOT_COOLDOWN
            else:
                bullets.append(Bullet.from_tank(self.x, self.y, self.size, self.dir, is_player=False))
                self.cooldown = ENEMY_SHOOT_COOLDOWN

    def draw(self, screen):
        draw_y = self.render_y + ARENA_Y
        x = int(self.render_x)

        if self.original_image:
            blit_tank(screen, self.original_image, self.render_x, draw_y, self.size, self.dir)
        else:
            body_color = BOSS_COLOR if self.is_boss else ENEMY_COLOR
            pygame.draw.rect(screen, body_color, (x, draw_y, self.size, self.size))

        if self.is_boss:
            hp_ratio = max(0, self.hp) / BOSS_HP
            pygame.draw.rect(screen, (50, 50, 50), (x, draw_y - 6, self.size, 4))
            pygame.draw.rect(screen, (255, 50, 50), (x, draw_y - 6, self.size * hp_ratio, 4))
