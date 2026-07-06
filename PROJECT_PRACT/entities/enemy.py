# entities/enemy.py
import pygame
import random
from settings import *
from entities.bullet import Bullet

class Coin:
    """Класс лута, выпадающего из врагов"""
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 8
        self.float_offset = 0.0
        self.float_dir = 0.2

    def update(self):
        # Анимация "парения" монетки вверх-вниз
        self.float_offset += self.float_dir
        if self.float_offset > 3 or self.float_offset < -3:
            self.float_dir *= -1

    def draw(self, screen):
        draw_y = self.y + self.float_offset
        # Основной золотой круг
        pygame.draw.circle(screen, COIN_COLOR, (int(self.x), int(draw_y)), self.radius)
        # Внутренний контур для объема (чеканка)
        pygame.draw.circle(screen, (200, 150, 0), (int(self.x), int(draw_y)), self.radius - 3)

class Enemy:
    def __init__(self, x, y, is_boss=False):
        self.x = x
        self.y = y
        self.is_boss = is_boss
        
        # Подтягиваем баланс из настроек
        self.size = 56 if is_boss else 28
        self.hp = BOSS_HP if is_boss else ENEMY_HP
        self.base_speed = BOSS_SPEED if is_boss else ENEMY_SPEED # Сохраняем базовую скорость для кустов
        
        self.dir = "down"
        self.cooldown = 0
        self.move_timer = 0 # Таймер ИИ для смены направления

        # --- ЗАГРУЗКА СПРАЙТОВ ВРАГОВ ---
        self.original_image = None
        # Оставляем только красные танки для всех врагов
        sprite_file = "танк(враг).png"
        
        try:
            img = pygame.image.load(sprite_file).convert_alpha()
            # Масштабируем картинку: обычный танк будет 28x28, Босс — 56x56
            self.original_image = pygame.transform.scale(img, (self.size, self.size))
        except FileNotFoundError:
            print(f"ВНИМАНИЕ: Спрайт '{sprite_file}' не найден. Включена заглушка.")

    def move(self, dx, dy, dungeon, player, enemies):
        """Плавное скольжение вдоль стен и столкновение с другими танками"""
        collided = False

        # Пробуем двинуться по X
        if dx != 0:
            new_x = self.x + dx
            if not dungeon.check_collision(new_x, self.y, self.size):
                # Проверка столкновения с игроком и другими врагами
                can_move = True
                my_rect = pygame.Rect(new_x, self.y, self.size, self.size)
                player_rect = pygame.Rect(player.x, player.y, player.size, player.size)
                
                if my_rect.colliderect(player_rect):
                    can_move = False
                    
                if can_move:
                    for other in enemies:
                        if other is not self: # Не проверяем столкновение с самим собой
                            other_rect = pygame.Rect(other.x, other.y, other.size, other.size)
                            if my_rect.colliderect(other_rect):
                                can_move = False
                                break
                                
                if can_move:
                    self.x = new_x
                else:
                    collided = True
            else:
                collided = True
                
        # Пробуем двинуться по Y
        if dy != 0:
            new_y = self.y + dy
            if not dungeon.check_collision(self.x, new_y, self.size):
                can_move = True
                my_rect = pygame.Rect(self.x, new_y, self.size, self.size)
                player_rect = pygame.Rect(player.x, player.y, player.size, player.size)
                
                if my_rect.colliderect(player_rect):
                    can_move = False
                    
                if can_move:
                    for other in enemies:
                        if other is not self:
                            other_rect = pygame.Rect(other.x, other.y, other.size, other.size)
                            if my_rect.colliderect(other_rect):
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

        # ИИ: Выбор направления
        if self.move_timer <= 0:
            self.dir = random.choice(["up", "down", "left", "right"])
            # Босс прет как танк, реже меняя направление
            self.move_timer = random.randint(60, 120) if self.is_boss else random.randint(30, 90)

        # --- ФИЗИКА КУСТОВ (Замедление для врагов) ---
        actual_speed = self.base_speed
        if dungeon.is_in_bush(self.x, self.y, self.size):
            actual_speed *= BUSH_SLOWDOWN_MULTIPLIER

        # Вектор скорости
        dx, dy = 0, 0
        if self.dir == "up": dy = -actual_speed
        elif self.dir == "down": dy = actual_speed
        elif self.dir == "left": dx = -actual_speed
        elif self.dir == "right": dx = actual_speed

        # Если врезались в препятствие (стену или другой танк), сразу меняем курс
        if self.move(dx, dy, dungeon, player, enemies):
            self.dir = random.choice(["up", "down", "left", "right"])
            self.move_timer = random.randint(30, 90)

        # Боевая система (СМЕЩЕНИЕ ПУЛИ К ДУЛУ)
        fire_chance = BOSS_FIRE_CHANCE if self.is_boss else ENEMY_FIRE_CHANCE
        if random.random() < fire_chance and self.cooldown == 0:
            center_x = self.x + self.size // 2
            center_y = self.y + self.size // 2
            offset = self.size // 2 + 4 # Смещение к краю танка
            
            if self.is_boss:
                # Особая механика: Босс стреляет "Крестом"
                for d in ["up", "down", "left", "right"]:
                    bx, by = center_x, center_y
                    if d == "up": by -= offset
                    elif d == "down": by += offset
                    elif d == "left": bx -= offset
                    elif d == "right": bx += offset
                    bullets.append(Bullet(bx, by, d, is_player=False))
                self.cooldown = BOSS_SHOOT_COOLDOWN
            else:
                # Обычный выстрел по направлению движения
                bx, by = center_x, center_y
                if self.dir == "up": by -= offset
                elif self.dir == "down": by += offset
                elif self.dir == "left": bx -= offset
                elif self.dir == "right": bx += offset
                
                bullets.append(Bullet(bx, by, self.dir, is_player=False))
                self.cooldown = ENEMY_SHOOT_COOLDOWN

    def get_loot(self):
        """Вызывается при смерти врага. Возвращает список монеток."""
        loot = []
        drop_count = BOSS_COIN_DROP if self.is_boss else (1 if random.random() < COIN_DROP_CHANCE else 0)
        
        for _ in range(drop_count):
            # Раскидываем монетки вокруг трупа
            offset_x = random.randint(-20, 20)
            offset_y = random.randint(-20, 20)
            
            coin_x = self.x + self.size//2 + offset_x
            coin_y = self.y + self.size//2 + offset_y
            
            # ЗАЩИТА ОТ БАГОВ: Ограничиваем координаты, чтобы монетки не спавнились в стенах или за картой
            coin_x = max(TILE_SIZE, min(coin_x, WIDTH - TILE_SIZE))
            coin_y = max(UI_HEIGHT + TILE_SIZE, min(coin_y, HEIGHT - TILE_SIZE))

            loot.append(Coin(coin_x, coin_y))
            
        return loot

    def draw(self, screen):
        # Отрисовка танка (Спрайт или заглушка)
        if self.original_image:
            # --- ИСПРАВЛЕННОЕ ВРАЩЕНИЕ СПРАЙТА ---
            # Исходный спрайт смотрит ВНИЗ
            if self.dir == "down":
                rotated_img = self.original_image
            elif self.dir == "up":
                rotated_img = pygame.transform.rotate(self.original_image, 180)
            elif self.dir == "left":
                rotated_img = pygame.transform.rotate(self.original_image, -90)
            elif self.dir == "right":
                rotated_img = pygame.transform.rotate(self.original_image, 90)
            
            screen.blit(rotated_img, (self.x, self.y))
        else:
            # Заглушка, если файла нет
            body_color = BOSS_COLOR if self.is_boss else ENEMY_COLOR
            track_color = (40, 40, 40)
            barrel_color = (20, 20, 20)
            
            # 1. Гусеницы
            if self.dir in ["up", "down"]:
                pygame.draw.rect(screen, track_color, (self.x, self.y, self.size//4, self.size))
                pygame.draw.rect(screen, track_color, (self.x + self.size - self.size//4, self.y, self.size//4, self.size))
                pygame.draw.rect(screen, body_color, (self.x + self.size//4, self.y + self.size//8, self.size//2, self.size - self.size//4))
            else:
                pygame.draw.rect(screen, track_color, (self.x, self.y, self.size, self.size//4))
                pygame.draw.rect(screen, track_color, (self.x, self.y + self.size - self.size//4, self.size, self.size//4))
                pygame.draw.rect(screen, body_color, (self.x + self.size//8, self.y + self.size//4, self.size - self.size//4, self.size//2))

            # 2. Орудие
            center_x = self.x + self.size // 2
            center_y = self.y + self.size // 2
            barrel_length = self.size // 2 + 4
            barrel_thickness = 10 if self.is_boss else 6
            
            if self.dir == "up":
                pygame.draw.rect(screen, barrel_color, (center_x - barrel_thickness//2, self.y - 4, barrel_thickness, barrel_length))
            elif self.dir == "down":
                pygame.draw.rect(screen, barrel_color, (center_x - barrel_thickness//2, center_y, barrel_thickness, barrel_length))
            elif self.dir == "left":
                pygame.draw.rect(screen, barrel_color, (self.x - 4, center_y - barrel_thickness//2, barrel_length, barrel_thickness))
            elif self.dir == "right":
                pygame.draw.rect(screen, barrel_color, (center_x, center_y - barrel_thickness//2, barrel_length, barrel_thickness))

        # 3. Угрожающий индикатор здоровья для Босса
        if self.is_boss:
            hp_ratio = max(0, self.hp) / BOSS_HP
            bar_width = self.size
            
            # Темно-серая подложка
            pygame.draw.rect(screen, (50, 50, 50), (self.x, self.y - 15, bar_width, 6))
            # Красная полоса ХП
            pygame.draw.rect(screen, (255, 50, 50), (self.x, self.y - 15, bar_width * hp_ratio, 6))
            # Золотая рамка для эпичности
            pygame.draw.rect(screen, (255, 215, 0), (self.x, self.y - 15, bar_width, 6), 1)