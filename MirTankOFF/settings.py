import os
import sys
import unicodedata

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


def _normalize_name(name: str) -> str:
    return unicodedata.normalize("NFC", name).casefold()


def _resolve_in_dir(directory: str, filename: str) -> str:
    direct = os.path.join(directory, filename)
    if os.path.exists(direct):
        return direct

    target = _normalize_name(filename)
    try:
        for entry in os.listdir(directory):
            if _normalize_name(entry) == target:
                return os.path.join(directory, entry)
    except (FileNotFoundError, NotADirectoryError):
        pass

    return direct


def asset_path(filename: str) -> str:
    return _resolve_in_dir(ASSETS_DIR, filename)


def sound_path(filename: str) -> str:
    return _resolve_in_dir(SOUNDS_DIR, filename)


def music_path(filename: str) -> str:
    return _resolve_in_dir(MUSIC_DIR, filename)


def font_path(filename: str) -> str:
    return _resolve_in_dir(FONTS_DIR, filename)




TILE_SIZE = 16
COLS = 13
ROWS = 13

UI_HEIGHT = 36
ARENA_Y = UI_HEIGHT

WIDTH = COLS * TILE_SIZE  # 208
ARENA_HEIGHT = ROWS * TILE_SIZE  # 208
HEIGHT = UI_HEIGHT + ARENA_HEIGHT  # 244

FPS = 60
GLIDE_PIXELS_PER_FRAME = 1.5
DEFAULT_WINDOW_SCALE = 3



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



COIN_DROP_CHANCE = 0.55
BOSS_COIN_DROP = 15

HEAL_COST = 5

MAX_COINS = 999



TILE_EMPTY = 0
TILE_OBSTACLE = 1
TILE_WALL = 2
TILE_DOOR = 4
TILE_SHOP = 5
TILE_BUSH = 6



STATE_MENU = "MENU"
STATE_PLAYING = "PLAYING"
STATE_GAME_OVER = "GAME_OVER"
STATE_VICTORY = "VICTORY"
STATE_CONFIRM_EXIT = "CONFIRM_EXIT"



GAME_SETTINGS = {
    "music": True,
    "sounds": True,
    "difficulty": "СРЕДНЯЯ",
    "fullscreen": False,
}



DIFFICULTY_SETTINGS = {
    "ЛЕГКАЯ": {
        "player_hp": 5,
        "enemy_hp": 2,
        "boss_hp": 15,
        "enemy_speed_mult": 1.0,
        "enemy_fire_chance": 0.035,
        "boss_fire_chance": 0.04,
        "boss_shoot_cooldown": 100,
        "heal_cost": 3,
    },
    "СРЕДНЯЯ": {
        "player_hp": 4,
        "enemy_hp": 4,
        "boss_hp": 20,
        "enemy_speed_mult": 1.0,
        "enemy_fire_chance": 0.06,
        "boss_fire_chance": 0.09,
        "boss_shoot_cooldown": 70,
        "heal_cost": 5,
    },
    "СЛОЖНАЯ": {
        "player_hp": 3,
        "enemy_hp": 4,
        "boss_hp": 25,
        "enemy_speed_mult": 1.3,
        "enemy_fire_chance": 0.09,
        "boss_fire_chance": 0.14,
        "boss_shoot_cooldown": 50,
        "heal_cost": 8,
    },
}

DIFFICULTY_OPTIONS = ["ВСЕ", "ЛЕГКАЯ", "СРЕДНЯЯ", "СЛОЖНАЯ"]


def get_difficulty_settings():
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

def get_boss_shoot_cooldown():
    return get_difficulty_settings()["boss_shoot_cooldown"]