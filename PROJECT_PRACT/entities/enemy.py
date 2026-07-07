# entities/enemy.py
import pygame
import random
from settings import *
from entities.bullet import Bullet
from core.sprites import blit_tank


class Enemy:
    def __init__(self, x, y, is_boss=False):
        self.x = x
        self.y = y
        self.is_boss = is_boss

        self.size = BOSS_SIZE if is_boss else TANK_SIZE
        self.hp = BOSS_HP if is_boss else ENEMY_HP
        self.base_speed = BOSS_SPEED if is_boss else ENEMY_SPEED

        self.dir = "up"
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

    def move(self, dx, dy, dungeon, player, enemies):
        collided = False

        if dx != 0:
            new_x = self.x + dx
            if not dungeon.check_collision(new_x, self.y, self.size):
                can_move = True
                my_rect = pygame.Rect(new_x, self.y, self.size, self.size)
                if my_rect.colliderect(pygame.Rect(player.x, player.y, player.size, player.size)):
                    can_move = False
                if can_move:
                    for other in enemies:
                        if other is not self:
                            if my_rect.colliderect(pygame.Rect(other.x, other.y, other.size, other.size)):
                                can_move = False
                                break
                if can_move:
                    self.x = new_x
                else:
                    collided = True
            else:
                collided = True

        if dy != 0:
            new_y = self.y + dy
            if not dungeon.check_collision(self.x, new_y, self.size):
                can_move = True
                my_rect = pygame.Rect(self.x, new_y, self.size, self.size)
                if my_rect.colliderect(pygame.Rect(player.x, player.y, player.size, player.size)):
                    can_move = False
                if can_move:
                    for other in enemies:
                        if other is not self:
                            if my_rect.colliderect(pygame.Rect(other.x, other.y, other.size, other.size)):
                                can_move = False
                                break
                if can_move:
                    self.y = new_y
                else:
                    collided = True
            else:
                collided = True

        return collided

    def update(self, dungeon, bullets, player, enemies):
        if self.cooldown > 0:
            self.cooldown -= 1
        if self.move_timer > 0:
            self.move_timer -= 1

        if self.move_timer <= 0:
            self.dir = random.choice(["up", "down", "left", "right"])
            self.move_timer = random.randint(60, 120) if self.is_boss else random.randint(30, 90)

        actual_speed = self.base_speed
        if dungeon.is_in_bush(self.x, self.y, self.size):
            actual_speed *= BUSH_SLOWDOWN_MULTIPLIER

        dx, dy = 0, 0
        if self.dir == "up":
            dy = -actual_speed
        elif self.dir == "down":
            dy = actual_speed
        elif self.dir == "left":
            dx = -actual_speed
        elif self.dir == "right":
            dx = actual_speed

        if self.move(dx, dy, dungeon, player, enemies):
            self.dir = random.choice(["up", "down", "left", "right"])
            self.move_timer = random.randint(30, 90)

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
        draw_y = self.y + ARENA_Y
        if self.original_image:
            blit_tank(screen, self.original_image, self.x, draw_y, self.size, self.dir)
        else:
            body_color = BOSS_COLOR if self.is_boss else ENEMY_COLOR
            pygame.draw.rect(screen, body_color, (self.x, draw_y, self.size, self.size))

        if self.is_boss:
            hp_ratio = max(0, self.hp) / BOSS_HP
            pygame.draw.rect(screen, (50, 50, 50), (self.x, draw_y - 6, self.size, 4))
            pygame.draw.rect(screen, (255, 50, 50), (self.x, draw_y - 6, self.size * hp_ratio, 4))
