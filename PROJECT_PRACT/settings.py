# ==========================================
# 1. ЭКРАН (Battle City: 208×208, тайлы 16×16)
# ==========================================

import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def asset_path(filename):
    return os.path.join(BASE_DIR, filename)


TILE_SIZE = 16
COLS = 13
ROWS = 13

UI_HEIGHT = 16
ARENA_Y = UI_HEIGHT

WIDTH = COLS * TILE_SIZE          # 208
ARENA_HEIGHT = ROWS * TILE_SIZE     # 208
HEIGHT = UI_HEIGHT + ARENA_HEIGHT   # 224

FPS = 60
GRID_MOVE_DELAY = 10


# ==========================================
# 2. ЦВЕТА
# ==========================================

BLACK = (15, 15, 15)
WHITE = (240, 240, 240)

UI_BG = (30, 30, 35)

GREEN = (46, 204, 113)
RED = (231, 76, 60)

PLAYER_COLOR = (241, 196, 15)
ENEMY_COLOR = (231, 76, 60)
BOSS_COLOR = (150, 0, 0)

WALL_COLOR = (200, 200, 205)
OBSTACLE_COLOR = (180, 80, 40)
BUSH_COLOR = (106, 176, 76)

DOOR_OPEN = (46, 204, 113)
DOOR_CLOSED = (231, 76, 60)

SHOP_BG_COLOR = (40, 35, 25)

COIN_COLOR = (255, 215, 0)
HEART_COLOR = (255, 50, 70)


# ==========================================
# 3. ИГРОВОЙ БАЛАНС
# ==========================================

PLAYER_MAX_HP = 3
PLAYER_SPEED = 2
PLAYER_SHOOT_COOLDOWN = 20
PLAYER_I_FRAMES = 90

ENEMY_HP = 2
ENEMY_SPEED = 1.5
ENEMY_SHOOT_COOLDOWN = 60
ENEMY_FIRE_CHANCE = 0.02

BOSS_HP = 20
BOSS_SPEED = 1.2
BOSS_SHOOT_COOLDOWN = 35
BOSS_FIRE_CHANCE = 0.06

BULLET_SPEED = 5
BULLET_RADIUS_PLAYER = 2
BULLET_RADIUS_ENEMY = 2

BUSH_SLOWDOWN_MULTIPLIER = 0.4

TANK_SIZE = TILE_SIZE
BOSS_SIZE = TILE_SIZE * 2

# Sprite faces UP at 0°; pygame.transform.rotate uses CCW degrees
DIRECTION_ANGLES = {
    "up": 0,
    "down": 180,
    "left": 90,
    "right": -90,
}

DEFAULT_WINDOW_SCALE = 2


# ==========================================
# 4. КАРТА
# ==========================================

TILE_EMPTY = 0
TILE_OBSTACLE = 1
TILE_WALL = 2
TILE_DOOR = 4
TILE_SHOP = 5
TILE_BUSH = 6


# ==========================================
# 5. СОСТОЯНИЯ ИГРЫ
# ==========================================

STATE_MENU = "MENU"
STATE_PLAYING = "PLAYING"
STATE_GAME_OVER = "GAME_OVER"
STATE_VICTORY = "VICTORY"
STATE_CONFIRM_EXIT = "CONFIRM_EXIT"


# ==========================================
# 6. НАСТРОЙКИ ИГРЫ
# ==========================================

GAME_SETTINGS = {
    "music": True,
    "sounds": True,
    "difficulty": "СРЕДНЯЯ"
}


# ==========================================
# 7. НАСТРОЙКИ СЛОЖНОСТИ
# ==========================================

DIFFICULTY_SETTINGS = {
    "ЛЕГКАЯ": {
        "player_hp": 4,
        "enemy_speed": 1.2,
        "enemy_fire_chance": 0.015,
        "boss_hp": 16,
    },
    "СРЕДНЯЯ": {
        "player_hp": 3,
        "enemy_speed": 1.5,
        "enemy_fire_chance": 0.02,
        "boss_hp": 20,
    },
    "СЛОЖНАЯ": {
        "player_hp": 2,
        "enemy_speed": 2,
        "enemy_fire_chance": 0.03,
        "boss_hp": 28,
    }
}
