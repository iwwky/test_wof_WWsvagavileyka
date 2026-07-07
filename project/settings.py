# ==========================================
# 0. ПУТИ (не зависят от рабочей директории запуска)
# ==========================================

import os
import sys

if getattr(sys, "frozen", False):
    BASE_DIR = sys._MEIPASS
    DATA_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DATA_DIR = BASE_DIR

ASSETS_DIR = os.path.join(BASE_DIR, "assets")
SOUNDS_DIR = os.path.join(ASSETS_DIR, "sounds")
FONTS_DIR = os.path.join(ASSETS_DIR, "fonts")
MUSIC_DIR = os.path.join(ASSETS_DIR, "music")


def asset_path(filename: str) -> str:
    """Абсолютный путь к файлу в папке assets/."""
    return os.path.join(ASSETS_DIR, filename)


def sound_path(filename: str) -> str:
    """Абсолютный путь к звуковому файлу."""
    return os.path.join(SOUNDS_DIR, filename)


def font_path(filename: str) -> str:
    """Абсолютный путь к шрифту."""
    return os.path.join(FONTS_DIR, filename)


# ==========================================
# 1. ЭКРАН (Battle City: арена 208×208, тайлы 16×16)
# ==========================================

TILE_SIZE = 16
COLS = 13
ROWS = 13

UI_HEIGHT = 36
ARENA_Y = UI_HEIGHT

WIDTH = COLS * TILE_SIZE          # 208
ARENA_HEIGHT = ROWS * TILE_SIZE   # 208
HEIGHT = UI_HEIGHT + ARENA_HEIGHT  # 244

FPS = 60
GLIDE_PIXELS_PER_FRAME = 2
DEFAULT_WINDOW_SCALE = 3


# ==========================================
# 2. ЦВЕТА
# ==========================================

BLACK = (12, 14, 22)
WHITE = (240, 240, 245)

UI_BG = (22, 26, 38)
UI_ACCENT = (255, 196, 46)
UI_PANEL = (32, 38, 54)

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

DIRECTION_ANGLES = {
    "down": 0,
    "up": 180,
    "left": -90,
    "right": 90,
}


# ==========================================
# 4. ЭКОНОМИКА
# ==========================================

COIN_DROP_CHANCE = 0.5
BOSS_COIN_DROP = 15

HEAL_COST = 5

MAX_COINS = 999


# ==========================================
# 5. КАРТА
# ==========================================

TILE_EMPTY = 0
TILE_OBSTACLE = 1
TILE_WALL = 2
TILE_DOOR = 4
TILE_SHOP = 5
TILE_BUSH = 6


# ==========================================
# 6. СОСТОЯНИЯ ИГРЫ
# ==========================================

STATE_MENU = "MENU"
STATE_PLAYING = "PLAYING"
STATE_GAME_OVER = "GAME_OVER"
STATE_VICTORY = "VICTORY"
STATE_CONFIRM_EXIT = "CONFIRM_EXIT"


# ==========================================
# 7. НАСТРОЙКИ ИГРЫ
# ==========================================

GAME_SETTINGS = {
    "music": True,
    "sounds": True,
    "difficulty": "СРЕДНЯЯ",
    "fullscreen": False,
    "show_fps": False,
}


# ==========================================
# 8. НАСТРОЙКИ СЛОЖНОСТИ
# ==========================================

DIFFICULTY_SETTINGS = {
    "ЛЕГКАЯ": {
        "player_hp": 5,
        "enemy_hp": 2,
        "boss_hp": 25,
        "enemy_speed_mult": 1.0,
        "enemy_fire_chance": 0.012,
        "heal_cost": 3,
    },
    "СРЕДНЯЯ": {
        "player_hp": 4,
        "enemy_hp": 4,
        "boss_hp": 35,
        "enemy_speed_mult": 1.0,
        "enemy_fire_chance": 0.02,
        "heal_cost": 5,
    },
    "СЛОЖНАЯ": {
        "player_hp": 3,
        "enemy_hp": 4,
        "boss_hp": 50,
        "enemy_speed_mult": 1.3,
        "enemy_fire_chance": 0.03,
        "heal_cost": 8,
    },
}

DIFFICULTY_OPTIONS = ["ВСЕ", "ЛЕГКАЯ", "СРЕДНЯЯ", "СЛОЖНАЯ"]


def get_difficulty_settings():
    """Текущие параметры баланса для выбранной сложности."""
    return DIFFICULTY_SETTINGS.get(
        GAME_SETTINGS["difficulty"],
        DIFFICULTY_SETTINGS["СРЕДНЯЯ"],
    )


def get_player_max_hp():
    return get_difficulty_settings()["player_hp"]


def get_enemy_hp():
    return get_difficulty_settings()["enemy_hp"]


def get_boss_hp():
    return get_difficulty_settings()["boss_hp"]


def get_enemy_speed_mult():
    return get_difficulty_settings()["enemy_speed_mult"]


def get_heal_cost():
    return get_difficulty_settings()["heal_cost"]
