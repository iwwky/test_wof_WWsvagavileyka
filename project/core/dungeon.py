# core/dungeon.py
import pygame

from settings import *

DOOR_COLS = [COLS // 2 - 1, COLS // 2, COLS // 2 + 1]
DOOR_ROWS = [ROWS // 2 - 1, ROWS // 2, ROWS // 2 + 1]


def _place_doors(matrix, doors):
    """Три центральных тайла на каждой стене — как в Battle City."""
    if "top" in doors:
        for c in DOOR_COLS:
            matrix[0][c] = TILE_DOOR
    if "bottom" in doors:
        for c in DOOR_COLS:
            matrix[ROWS - 1][c] = TILE_DOOR
    if "left" in doors:
        for r in DOOR_ROWS:
            matrix[r][0] = TILE_DOOR
    if "right" in doors:
        for r in DOOR_ROWS:
            matrix[r][COLS - 1] = TILE_DOOR


def _apply_tiles(matrix, stones, bricks, bushes, safe_zones):
    for r, c in stones:
        if 0 < r < ROWS - 1 and 0 < c < COLS - 1 and (r, c) not in safe_zones:
            if matrix[r][c] == TILE_EMPTY:
                matrix[r][c] = TILE_WALL

    for r, c in bricks:
        if 0 < r < ROWS - 1 and 0 < c < COLS - 1 and (r, c) not in safe_zones:
            if matrix[r][c] == TILE_EMPTY:
                matrix[r][c] = TILE_OBSTACLE

    for r, c in bushes:
        if 0 < r < ROWS - 1 and 0 < c < COLS - 1 and (r, c) not in safe_zones:
            if matrix[r][c] == TILE_EMPTY:
                matrix[r][c] = TILE_BUSH


def _build_safe_zones(extra_spawns=None):
    safe = set()
    spawns = [
        (2, 2), (2, 10), (10, 2), (10, 10), (6, 6),
        (2, 6), (10, 6), (6, 2), (6, 10),
    ]
    door_safe = [
        (1, 5), (1, 6), (1, 7),
        (11, 5), (11, 6), (11, 7),
        (5, 1), (6, 1), (7, 1),
        (5, 11), (6, 11), (7, 11),
    ]
    spawns.extend(door_safe)
    if extra_spawns:
        spawns.extend(extra_spawns)

    for sr, sc in spawns:
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                safe.add((sr + dr, sc + dc))
    return safe


# Статические шаблоны — насыщенные, как в классическом Battle City.
ROOM_LAYOUTS = {
    "spawn": {
        "stones": [(4, 5), (4, 7), (8, 5), (8, 7)],
        "bricks": [(6, 4), (6, 8), (4, 6), (8, 6)],
        "bushes": [
            (3, 5), (3, 7), (5, 4), (5, 8), (7, 4), (7, 8), (9, 5), (9, 7),
            (2, 3), (2, 9), (10, 3), (10, 9),
        ],
    },
    "arena_fortress": {
        "stones": [(3, 3), (3, 9), (9, 3), (9, 9)],
        "bricks": [
            (r, 5) for r in range(4, 9) if r != 6
        ] + [
            (r, 7) for r in range(4, 9) if r != 6
        ] + [
            (5, c) for c in range(4, 9)
        ] + [
            (7, c) for c in range(4, 9) if c not in (5, 6, 7)
        ],
        "bushes": [
            (2, c) for c in range(2, 11)
        ] + [(4, 2), (4, 10), (6, 3), (6, 9), (8, 2), (8, 10)],
    },
    "arena_garden": {
        "stones": [(4, 4), (4, 8), (8, 4), (8, 8)],
        "bricks": [
            (6, c) for c in range(3, 10) if c not in (5, 6, 7)
        ] + [(c, 6) for c in (4, 5, 7, 8)],
        "bushes": [
            (2, 3), (2, 4), (2, 8), (2, 9),
            (3, 2), (4, 2), (8, 2), (9, 2),
            (10, 3), (10, 4), (10, 8), (10, 9),
            (3, 10), (4, 10), (8, 10), (9, 10),
            (5, 3), (7, 3), (5, 9), (7, 9),
        ],
    },
    "arena_bridge": {
        "stones": [(3, 3), (3, 9), (9, 3), (9, 9), (6, 6)],
        "bricks": [
            (5, c) for c in range(4, 9)
        ] + [
            (7, c) for c in range(4, 9) if c not in (5, 6, 7)
        ] + [
            (3, 5), (4, 5), (8, 5), (9, 5),
            (3, 7), (4, 7), (8, 7), (9, 7),
        ],
        "bushes": [
            (2, 5), (2, 6), (2, 7), (10, 5), (10, 6), (10, 7),
            (4, 2), (6, 2), (8, 2), (4, 10), (6, 10), (8, 10),
        ],
    },
    "shop": {
        "stones": [(5, 4), (5, 8), (7, 4), (7, 8)],
        "bricks": [(4, 6), (8, 6), (6, 4), (6, 8), (3, 3), (3, 9), (9, 3), (9, 9)],
        "bushes": [(6, 5), (6, 6), (6, 7), (2, 6), (10, 6), (5, 2), (7, 2), (5, 10), (7, 10)],
        "shop_tiles": [(6, 5), (6, 6)],
    },
    "boss": {
        "stones": [(3, 3), (3, 9), (9, 3), (9, 9), (5, 3), (5, 9)],
        "bricks": [
            (10, c) for c in range(3, 10) if c not in (5, 6, 7)
        ] + [
            (c, 5) for c in range(8, 11)
        ] + [
            (c, 7) for c in range(8, 11)
        ] + [
            (4, 5), (4, 7), (8, 5), (8, 7),
        ],
        "bushes": [(2, 2), (2, 10), (4, 2), (4, 10), (2, 5), (2, 7), (10, 5), (10, 7)],
    },
}

ROOM_LAYOUT_KEY = {
    (0, 0): "spawn",
    (-1, 0): "arena_fortress",
    (1, 0): "arena_garden",
    (1, 1): "shop",
    (0, 1): "arena_bridge",
    (0, 2): "boss",
}


def generate_room_matrix(doors, room_type, pos):
    matrix = [[TILE_EMPTY for _ in range(COLS)] for _ in range(ROWS)]

    for r in range(ROWS):
        for c in range(COLS):
            if r == 0 or r == ROWS - 1 or c == 0 or c == COLS - 1:
                matrix[r][c] = TILE_WALL

    _place_doors(matrix, doors)

    layout_key = ROOM_LAYOUT_KEY.get(pos, "spawn")
    layout = ROOM_LAYOUTS[layout_key]

    extra_spawns = [(3, 6), (4, 6), (5, 6)] if room_type == "boss" else []
    safe_zones = _build_safe_zones(extra_spawns)

    _apply_tiles(
        matrix,
        layout.get("stones", []),
        layout.get("bricks", []),
        layout.get("bushes", []),
        safe_zones,
    )

    if room_type == "shop":
        for r, c in layout.get("shop_tiles", [(6, 5), (6, 6)]):
            matrix[r][c] = TILE_SHOP

    return matrix


class Dungeon:
    def __init__(self):
        self.sprites = {}
        self.load_sprite("brick", "Кирпич.png")
        self.load_sprite("stone", "Стена.png")
        self.load_sprite("door", "ворота.png")

        self.bush_sprites = []
        for b_name in ["куст дефолт.png", "куст с черникой.png", "куст бручника.png"]:
            try:
                img = pygame.image.load(asset_path(b_name)).convert_alpha()
                self.bush_sprites.append(img)
            except FileNotFoundError:
                pass

        self.rooms = {
            (0, 0): {"type": "spawn", "doors": ["top", "left", "right"], "cleared": True},
            (-1, 0): {"type": "arena", "doors": ["right"], "cleared": False},
            (1, 0): {"type": "arena", "doors": ["left", "top"], "cleared": False},
            (1, 1): {"type": "shop", "doors": ["bottom"], "cleared": True},
            (0, 1): {"type": "arena", "doors": ["bottom", "top"], "cleared": False},
            (0, 2): {"type": "boss", "doors": ["bottom"], "cleared": False},
        }

        for pos, data in self.rooms.items():
            data["matrix"] = generate_room_matrix(data["doors"], data["type"], pos)

        self.current_pos = (0, 0)
        self.doors_locked = False
        self.boss_unlocked = False

    def load_sprite(self, name, filename):
        try:
            img = pygame.image.load(asset_path(filename)).convert_alpha()
            self.sprites[name] = img
        except FileNotFoundError:
            self.sprites[name] = None

    def get_matrix(self):
        return self.rooms[self.current_pos]["matrix"]

    def _is_door_passable(self, row, col):
        matrix = self.get_matrix()
        if matrix[row][col] != TILE_DOOR:
            return False
        if self.doors_locked:
            return False
        if not self.boss_unlocked and self.current_pos == (0, 1) and row == 0:
            return False
        return True

    def get_passage_at(self, col, row):
        """Направление прохода, если танк стоит на открытой двери."""
        if row == 0 and col in DOOR_COLS and self._is_door_passable(0, col):
            return "top"
        if row == ROWS - 1 and col in DOOR_COLS and self._is_door_passable(ROWS - 1, col):
            return "bottom"
        if col == 0 and row in DOOR_ROWS and self._is_door_passable(row, 0):
            return "left"
        if col == COLS - 1 and row in DOOR_ROWS and self._is_door_passable(row, COLS - 1):
            return "right"
        return None

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
                    rects.append(pygame.Rect(c * TILE_SIZE, ARENA_Y + r * TILE_SIZE, TILE_SIZE, TILE_SIZE))
        return rects

    def is_in_bush(self, x, y, size):
        center_x = x + size // 2
        center_y = y + size // 2
        col = int(center_x // TILE_SIZE)
        row = int(center_y // TILE_SIZE)
        if 0 <= row < ROWS and 0 <= col < COLS:
            return self.get_matrix()[row][col] == TILE_BUSH
        return False

    def check_collision(self, x, y, size=TANK_SIZE):
        matrix = self.get_matrix()
        start_col = int(x // TILE_SIZE)
        end_col = int((x + size - 1) // TILE_SIZE)
        start_row = int(y // TILE_SIZE)
        end_row = int((y + size - 1) // TILE_SIZE)

        for row in range(start_row, end_row + 1):
            for col in range(start_col, end_col + 1):
                if 0 <= row < ROWS and 0 <= col < COLS:
                    tile = matrix[row][col]
                    if tile in (TILE_WALL, TILE_OBSTACLE, TILE_SHOP):
                        return True
                    if tile == TILE_DOOR:
                        if self.doors_locked:
                            return True
                        if not self.boss_unlocked and self.current_pos == (0, 1) and row == 0:
                            return True
                else:
                    return True
        return False

    def draw(self, screen):
        matrix = self.get_matrix()
        room_type = self.rooms[self.current_pos]["type"]

        floor_color = SHOP_BG_COLOR if room_type == "shop" else BLACK
        pygame.draw.rect(screen, floor_color, (0, ARENA_Y, WIDTH, ARENA_HEIGHT))

        for r in range(ROWS):
            for c in range(COLS):
                tile = matrix[r][c]
                if tile in (TILE_EMPTY, TILE_BUSH):
                    continue

                rx = c * TILE_SIZE
                ry = ARENA_Y + r * TILE_SIZE
                rect = (rx, ry, TILE_SIZE, TILE_SIZE)

                if tile == TILE_WALL:
                    if self.sprites["stone"]:
                        screen.blit(self.sprites["stone"], (rx, ry))
                    else:
                        pygame.draw.rect(screen, WALL_COLOR, rect)

                elif tile == TILE_OBSTACLE:
                    if self.sprites["brick"]:
                        screen.blit(self.sprites["brick"], (rx, ry))
                    else:
                        pygame.draw.rect(screen, OBSTACLE_COLOR, rect)

                elif tile == TILE_DOOR:
                    is_boss_door = self.current_pos == (0, 1) and r == 0
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
                    pygame.draw.rect(screen, COIN_COLOR, rect, 1)
                    pygame.draw.rect(screen, HEART_COLOR, (rx + 6, ry + 3, 4, 10))
                    pygame.draw.rect(screen, HEART_COLOR, (rx + 3, ry + 6, 10, 4))

    def draw_top_layer(self, screen):
        matrix = self.get_matrix()
        for r in range(ROWS):
            for c in range(COLS):
                if matrix[r][c] == TILE_BUSH:
                    rx = c * TILE_SIZE
                    ry = ARENA_Y + r * TILE_SIZE

                    if self.bush_sprites:
                        bush_idx = (r + c * 3) % len(self.bush_sprites)
                        screen.blit(self.bush_sprites[bush_idx], (rx, ry))
                    else:
                        pygame.draw.rect(screen, BUSH_COLOR, (rx, ry, TILE_SIZE, TILE_SIZE))
