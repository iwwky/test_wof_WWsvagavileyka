# core/dungeon.py
import pygame
from settings import *

def generate_room_matrix(doors, room_type, pos):
    """Генерирует статичную, красивую матрицу комнаты на основе её координат"""
    matrix = [[TILE_EMPTY for _ in range(COLS)] for _ in range(ROWS)]
    
    for r in range(ROWS):
        for c in range(COLS):
            if r == 0 or r == ROWS - 1 or c == 0 or c == COLS - 1:
                matrix[r][c] = TILE_WALL 

    mid_r, mid_c = ROWS // 2, COLS // 2
    if "top" in doors:
        matrix[0][mid_c - 1] = matrix[0][mid_c] = TILE_DOOR
    if "bottom" in doors:
        matrix[ROWS - 1][mid_c - 1] = matrix[ROWS - 1][mid_c] = TILE_DOOR
    if "left" in doors:
        matrix[mid_r - 1][0] = matrix[mid_r][0] = TILE_DOOR
    if "right" in doors:
        matrix[mid_r - 1][COLS - 1] = matrix[mid_r][COLS - 1] = TILE_DOOR

    safe_zones = set()
    spawns = [(3, 3), (3, 20), (16, 12)]
    doors_safe = [(1, 11), (1, 12), (18, 11), (18, 12), (9, 1), (10, 1), (9, 22), (10, 22)]
    spawns.extend(doors_safe)

    if room_type == "boss":
        spawns.append((4, 12)) 

    for sr, sc in spawns:
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                safe_zones.add((sr + dr, sc + dc))

    stones, bricks, bushes = [], [], []

    if room_type == "spawn":
        stones = [(7, 9), (7, 14), (12, 9), (12, 14)]
        bushes = [(6, 9), (8, 9), (7, 8), (7, 10),
                  (6, 14), (8, 14), (7, 13), (7, 15),
                  (11, 9), (13, 9), (12, 8), (12, 10),
                  (11, 14), (13, 14), (12, 13), (12, 15)]

    elif room_type == "arena":
        if pos == (-1, 0):
            stones = [(r, c) for r in [6, 13] for c in [7, 16]]
            bricks = [(r, c) for r in range(4, 16) for c in [5, 18] if r not in [9, 10]] + \
                     [(r, c) for r in [4, 15] for c in range(6, 18) if c not in [11, 12]] + \
                     [(r, c) for r in range(8, 12) for c in [9, 14] if r not in [9, 10]]
            bushes = [(r, c) for r in range(2, 18) for c in [2, 21]]
            
        elif pos == (1, 0):
            stones = [(7, 8), (7, 15), (12, 8), (12, 15)]
            bricks = [(r, c) for r in [7, 12] for c in range(9, 15) if c not in [11, 12]] + \
                     [(r, c) for r in range(8, 12) for c in [8, 15] if r not in [9, 10]]
            bushes = [(r, c) for r in range(3, 17) for c in range(3, 21) if r not in range(6, 14) and c not in range(7, 17) and (r+c)%3 == 0]
            
        elif pos == (0, 1):
            stones = [(r, c) for r in range(4, 16, 4) for c in range(4, 20, 5)]
            bricks = [(r, c) for r in range(8, 12) for c in [11, 12] if r not in [9, 10]] + \
                     [(r, c) for r in [9, 10] for c in range(9, 15) if c not in [11, 12]]
            bushes = [(r, c) for r in range(2, 18) for c in range(2, 22) if (r+c) % 2 == 0]

    elif room_type == "shop":
        stones = [(8, 10), (8, 13), (11, 10), (11, 13)]
        bushes = [(r, c) for r in [9, 10] for c in [9, 14]]
        matrix[mid_r][mid_c - 1] = matrix[mid_r][mid_c] = TILE_SHOP

    elif room_type == "boss":
        stones = [(r, c) for r in range(3, 8) for c in [5, 18]] + \
                 [(14, 7), (14, 16), (10, 5), (10, 18)]
        bricks = [(r, c) for r in [8] for c in range(5, 19) if c not in range(9, 15)] + \
                 [(15, c) for c in range(6, 18) if c not in range(10, 14)]
        bushes = [(r, c) for r in range(2, 6) for c in [2, 3, 20, 21]]

    for r, c in stones:
        if 0 < r < ROWS - 1 and 0 < c < COLS - 1 and (r, c) not in safe_zones:
            if matrix[r][c] == TILE_EMPTY: matrix[r][c] = TILE_WALL
            
    for r, c in bricks:
        if 0 < r < ROWS - 1 and 0 < c < COLS - 1 and (r, c) not in safe_zones:
            if matrix[r][c] == TILE_EMPTY: matrix[r][c] = TILE_OBSTACLE
            
    for r, c in bushes:
        if 0 < r < ROWS - 1 and 0 < c < COLS - 1 and (r, c) not in safe_zones:
            if matrix[r][c] == TILE_EMPTY: matrix[r][c] = TILE_BUSH

    return matrix

class Dungeon:
    def __init__(self):
        self.sprites = {}
        self.load_sprite("brick", "Кирпич.png")
        self.load_sprite("stone", "Стена.png") 
        self.load_sprite("door", "ворота.png")
        
        self.bush_sprites = []
        for b_name in ["куст дефолт.png", "куст с черникой.png", "куст бручника.png"]:
            try:
                img = pygame.image.load(b_name).convert_alpha()
                self.bush_sprites.append(pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE)))
            except FileNotFoundError:
                pass
        
        self.rooms = {
            (0, 0): {"type": "spawn", "doors": ["top", "left", "right"], "cleared": True},
            (-1, 0): {"type": "arena", "doors": ["right"], "cleared": False},
            (1, 0): {"type": "arena", "doors": ["left", "top"], "cleared": False},
            (1, 1): {"type": "shop", "doors": ["bottom"], "cleared": True},
            (0, 1): {"type": "arena", "doors": ["bottom", "top"], "cleared": False},
            (0, 2): {"type": "boss", "doors": ["bottom"], "cleared": False}
        }
        
        for pos, data in self.rooms.items():
            data["matrix"] = generate_room_matrix(data["doors"], data["type"], pos)
            
        self.current_pos = (0, 0)
        self.doors_locked = False
        self.boss_unlocked = False # Флаг доступности комнаты Босса

    def load_sprite(self, name, filename):
        try:
            img = pygame.image.load(filename).convert_alpha()
            self.sprites[name] = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
        except FileNotFoundError:
            self.sprites[name] = None

    def get_matrix(self):
        return self.rooms[self.current_pos]["matrix"]

    def lock_doors(self):
        self.doors_locked = True

    def unlock_doors(self):
        self.doors_locked = False
        self.rooms[self.current_pos]["cleared"] = True

    def get_shop_rects(self):
        rects = []
        matrix = self.get_matrix()
        for r in range(ROWS):
            for c in range(COLS):
                if matrix[r][c] == TILE_SHOP:
                    rects.append(pygame.Rect(c * TILE_SIZE, UI_HEIGHT + r * TILE_SIZE, TILE_SIZE, TILE_SIZE))
        return rects

    def is_in_bush(self, x, y, size):
        center_x = x + size // 2
        center_y = y + size // 2
        col = int(center_x // TILE_SIZE)
        row = int((center_y - UI_HEIGHT) // TILE_SIZE)
        if 0 <= row < ROWS and 0 <= col < COLS:
            return self.get_matrix()[row][col] == TILE_BUSH
        return False

    def check_collision(self, x, y, size=28):
        matrix = self.get_matrix()
        start_col = int(x // TILE_SIZE)
        end_col = int((x + size - 1) // TILE_SIZE)
        start_row = int((y - UI_HEIGHT) // TILE_SIZE)
        end_row = int((y + size - 1 - UI_HEIGHT) // TILE_SIZE)
        
        for row in range(start_row, end_row + 1):
            for col in range(start_col, end_col + 1):
                if 0 <= row < ROWS and 0 <= col < COLS:
                    tile = matrix[row][col]
                    if tile in [TILE_WALL, TILE_OBSTACLE, TILE_SHOP]: 
                        return True
                    if tile == TILE_DOOR:
                        if self.doors_locked: 
                            return True
                        # Блокируем верхнюю дверь к боссу, если он не разблокирован
                        if not self.boss_unlocked and self.current_pos == (0, 1) and row == 0:
                            return True
                else:
                    return True
        return False

    def draw(self, screen):
        matrix = self.get_matrix()
        room_type = self.rooms[self.current_pos]["type"]

        floor_color = SHOP_BG_COLOR if room_type == "shop" else BLACK
        pygame.draw.rect(screen, floor_color, (0, UI_HEIGHT, WIDTH, ROWS * TILE_SIZE))

        for r in range(ROWS):
            for c in range(COLS):
                tile = matrix[r][c]
                if tile in [TILE_EMPTY, TILE_BUSH]:
                    continue

                rx = c * TILE_SIZE
                ry = UI_HEIGHT + r * TILE_SIZE
                rect = (rx, ry, TILE_SIZE, TILE_SIZE)

                if tile == TILE_WALL:
                    if self.sprites["stone"]:
                        screen.blit(self.sprites["stone"], (rx, ry))
                    else:
                        pygame.draw.rect(screen, WALL_COLOR, rect)
                        pygame.draw.line(screen, (150, 150, 155), (rx, ry), (rx + TILE_SIZE, ry), 2)
                        pygame.draw.line(screen, (60, 60, 65), (rx, ry + TILE_SIZE), (rx + TILE_SIZE, ry + TILE_SIZE), 2)

                elif tile == TILE_OBSTACLE:
                    if self.sprites["brick"]:
                        screen.blit(self.sprites["brick"], (rx, ry))
                    else:
                        pygame.draw.rect(screen, OBSTACLE_COLOR, rect)
                        pygame.draw.line(screen, (100, 30, 10), (rx, ry + 10), (rx + TILE_SIZE, ry + 10), 2)
                        pygame.draw.line(screen, (100, 30, 10), (rx, ry + 22), (rx + TILE_SIZE, ry + 22), 2)

                elif tile == TILE_DOOR:
                    # Проверяем, это ли та самая дверь к Боссу
                    is_boss_door = (self.current_pos == (0, 1) and r == 0)
                    # Дверь закрыта если идет бой, ИЛИ если это дверь к боссу и он заблокирован
                    is_locked = self.doors_locked or (is_boss_door and not self.boss_unlocked)

                    if self.sprites["door"]:
                        screen.blit(self.sprites["door"], (rx, ry))
                        if is_locked:
                            lock_surf = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
                            lock_surf.fill((200, 0, 0, 100)) 
                            screen.blit(lock_surf, (rx, ry))
                    else:
                        color = DOOR_CLOSED if is_locked else DOOR_OPEN
                        pygame.draw.rect(screen, color, rect)

                elif tile == TILE_SHOP:
                    pygame.draw.rect(screen, (139, 69, 19), rect)
                    pygame.draw.rect(screen, COIN_COLOR, (rx, ry, TILE_SIZE, TILE_SIZE), 2)
                    pygame.draw.rect(screen, HEART_COLOR, (rx + 12, ry + 6, 8, 20))
                    pygame.draw.rect(screen, HEART_COLOR, (rx + 6, ry + 12, 20, 8))

    def draw_top_layer(self, screen):
        matrix = self.get_matrix()
        for r in range(ROWS):
            for c in range(COLS):
                if matrix[r][c] == TILE_BUSH:
                    rx = c * TILE_SIZE
                    ry = UI_HEIGHT + r * TILE_SIZE
                    
                    if self.bush_sprites:
                        bush_idx = (r + c * 3) % len(self.bush_sprites)
                        screen.blit(self.bush_sprites[bush_idx], (rx, ry))
                    else:
                        bush_surf = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
                        pygame.draw.rect(bush_surf, (106, 176, 76, 200), (0, 0, TILE_SIZE, TILE_SIZE))
                        pygame.draw.circle(bush_surf, (50, 120, 50, 255), (8, 8), 6)
                        pygame.draw.circle(bush_surf, (50, 120, 50, 255), (24, 20), 8)
                        screen.blit(bush_surf, (rx, ry))