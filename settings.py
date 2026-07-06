# ==========================================
# 1. ЭКРАН
# ==========================================

TILE_SIZE = 32
COLS = 24
ROWS = 20

UI_HEIGHT = 60

WIDTH = COLS * TILE_SIZE
HEIGHT = ROWS * TILE_SIZE + UI_HEIGHT

FPS = 60


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
PLAYER_SPEED = 4
PLAYER_SHOOT_COOLDOWN = 20
PLAYER_I_FRAMES = 90

ENEMY_HP = 2
ENEMY_SPEED = 2
ENEMY_SHOOT_COOLDOWN = 60
ENEMY_FIRE_CHANCE = 0.02

BOSS_HP = 30
BOSS_SPEED = 1.5
BOSS_SHOOT_COOLDOWN = 35
BOSS_FIRE_CHANCE = 0.06

BULLET_SPEED = 10
BULLET_RADIUS_PLAYER = 4
BULLET_RADIUS_ENEMY = 5

BUSH_SLOWDOWN_MULTIPLIER = 0.3


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
    "difficulty": "СРЕДНЯЯ"
}


# ==========================================
# 8. НАСТРОЙКИ СЛОЖНОСТИ
# ==========================================

DIFFICULTY_SETTINGS = {
    "ЛЕГКАЯ": {
        "player_hp": 4,
        "enemy_speed": 1.6,
        "enemy_fire_chance": 0.015,
        "boss_hp": 24,
        "heal_cost": 3,
    },
    "СРЕДНЯЯ": {
        "player_hp": 3,
        "enemy_speed": 2,
        "enemy_fire_chance": 0.02,
        "boss_hp": 30,
        "heal_cost": 5,
    },
    "СЛОЖНАЯ": {
        "player_hp": 2,
        "enemy_speed": 2.6,
        "enemy_fire_chance": 0.03,
        "boss_hp": 40,
        "heal_cost": 8,
    }
}