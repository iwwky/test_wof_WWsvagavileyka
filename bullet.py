# entities/bullet.py
import pygame
from settings import *

class Bullet:
    def __init__(self, x, y, direction, is_player):
        self.x = x
        self.y = y
        self.dir = direction
        self.is_player = is_player
        
        # Подтягиваем баланс из глобальных настроек
        self.speed = BULLET_SPEED
        self.radius = BULLET_RADIUS_PLAYER if is_player else BULLET_RADIUS_ENEMY
        self.active = True # Флаг: если False, пуля удаляется из списка в главном цикле

    def update(self, dungeon):
        # 1. Полет снаряда
        if self.dir == "up": self.y -= self.speed
        elif self.dir == "down": self.y += self.speed
        elif self.dir == "left": self.x -= self.speed
        elif self.dir == "right": self.x += self.speed

        # 2. Проверка попадания в стены и укрытия
        col = int(self.x // TILE_SIZE)
        # ВАЖНО: Вычитаем UI_HEIGHT, так как игровая матрица начинается ниже интерфейса
        row = int((self.y - UI_HEIGHT) // TILE_SIZE)
        
        matrix = dungeon.get_matrix()
        
        # Проверяем, не вылетела ли пуля за пределы окна
        if 0 <= row < ROWS and 0 <= col < COLS:
            tile = matrix[row][col]
            
            if tile == TILE_OBSTACLE:
                # Попадание в кирпич разрушает его
                matrix[row][col] = TILE_EMPTY
                self.active = False
            elif tile == TILE_WALL:
                # Попадание в бетон просто уничтожает пулю
                self.active = False
            elif tile == TILE_SHOP:
                # Магазин/Сундук пуленепробиваемый
                self.active = False
            elif tile == TILE_DOOR and dungeon.doors_locked:
                # Во время боя двери закрыты и работают как бетон
                self.active = False
        else:
            # Пуля улетела за границу экрана
            self.active = False

    def draw(self, screen):
        # 3. Отрисовка с эффектом свечения (двойной круг)
        if self.is_player:
            # Пуля игрока - Желтая
            outer_color = (200, 150, 0) # Темно-желтый/оранжевый ореол
            inner_color = (255, 255, 0) # Ярко-желтое ядро
        else:
            # Пуля врага - Красная
            outer_color = (150, 0, 0)   # Темно-красный ореол
            inner_color = (255, 0, 0)   # Ярко-красное ядро

        # Отрисовка внешнего ореола (Glow)
        pygame.draw.circle(screen, outer_color, (int(self.x), int(self.y)), self.radius + 2)
        # Отрисовка внутреннего горячего ядра
        pygame.draw.circle(screen, inner_color, (int(self.x), int(self.y)), self.radius)