import pygame

from settings import *

DOOR_COLS = [COLS // 2 - 1, COLS // 2, COLS // 2 + 1]
DOOR_ROWS = [ROWS // 2 - 1, ROWS // 2, ROWS // 2 + 1]


def _place_doors(matrix, doors):
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


TILE_FROM_CHAR = {
    "#": TILE_WALL,
    "B": TILE_OBSTACLE,
    "*": TILE_BUSH,
    ".": TILE_EMPTY,
    "D": TILE_WALL,
    "C": TILE_SHOP,
    "С": TILE_SHOP,
}


def _matrix_from_ascii(ascii_map):
    matrix = [[TILE_EMPTY for _ in range(COLS)] for _ in range(ROWS)]
    for r, row_str in enumerate(ascii_map):
        for c, ch in enumerate(row_str):
            matrix[r][c] = TILE_FROM_CHAR.get(ch, TILE_EMPTY)
    return matrix


SPAWN_ROOM_MAP = [
    "#####DDD#####",
    "#***#...#***#",
    "#**#.....#**#",
    "#*#.......#*#",
    "##.........##",
    "D...........D",
    "D...........D",
    "D...........D",
    "##.........##",
    "#*#.......#*#",
    "#**#.....#**#",
    "#***#***#***#",
    "#############",
]

#левая
ARENA_FORTRESS_MAP = [
    "#############",
    "#...B......B#",
    "#...B......*#",
    "#..BB......*#",
    "#BBBB.#*..###",
    "#..*####BB#.D",
    "#...B#**..#.D",
    "#.*.B.....B.D",
    "#####..***B.#",
    "#**.....#B*.#",
    "#.......#...#",
    "#B.**...#*.B#",
    "#############",
]

#правая
ARENA_GARDEN_MAP = [
    "#####DDD#####",
    "#*..#...#.**#",
    "#**......**.#",
    "#.**....**..#",
    "##.*..B....##",
    "D....B#B....#",
    "D...B###B...#",
    "D....B#B....#",
    "##....B..*.##",
    "#...*....**.#",
    "#.**......**#",
    "#**.#...#..*#",
    "#############",
]

#верхняя
ARENA_BRIDGE_MAP = [
    "#####DDD#####",
    "#.......#.B.#",
    "#B#######.#.#",
    "#.........#.#",
    "#########B#.#",
    "#......#..#.#",
    "#.####B#B##.#",
    "#.#*.#.#.*#.#",
    "###....#.*###",
    "#*..*.......#",
    "#..*#...#**.#",
    "#...#...#...#",
    "#####DDD#####",
]

SHOP_ROOM_MAP = [
    "#############",
    "#СС.B......B#",
    "#СС.B......*#",
    "#..BB......*#",
    "#BBBB.#*..###",
    "D..*####BB#.#",
    "D...B#**..#.#",
    "D.*.B.....B.#",
    "#####..***B.#",
    "#**.....#B*.#",
    "#.......#...#",
    "#B.**...#*.B#",
    "#####DDD#####",
]

BOSS_ROOM_MAP = [
    "#############",
    "#***.....***#",
    "#*.........*#",
    "#*......##.*#",
    "#.*......#*.#",
    "#*.........*#",
    "#.*.......*.#",
    "#*.........*#",
    "#.*#......*.#",
    "#*.##......*#",
    "#*.........*#",
    "#***.....***#",
    "#############",
]

ROOM_MAPS = {
    (0, 0): SPAWN_ROOM_MAP,
    (-1, 0): ARENA_FORTRESS_MAP,
    (1, 0): ARENA_GARDEN_MAP,
    (0, 1): ARENA_BRIDGE_MAP,
    (1, 1): SHOP_ROOM_MAP,
    (0, 2): BOSS_ROOM_MAP,
}


def generate_room_matrix(doors, pos):
    matrix = _matrix_from_ascii(ROOM_MAPS[pos])
    _place_doors(matrix, doors)
    return matrix


class Dungeon:
    def __init__(self):
        self.sprites = {}
        self.load_sprite("brick", "Кирпич.png")
        self.load_sprite("stone", "Стена.png")
        self.load_sprite("door", "ворота.png")
        self.load_sprite("chest_closed", "сундук закрытый.png")
        self.load_sprite("chest_open", "сундук открытый.png")

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
            (1, 1): {"type": "shop", "doors": ["bottom"], "cleared": False, "shop_opened": False},
            (0, 1): {"type": "arena", "doors": ["bottom", "top"], "cleared": False},
            (0, 2): {"type": "boss", "doors": ["bottom"], "cleared": False},
        }

        for pos, data in self.rooms.items():
            data["matrix"] = generate_room_matrix(data["doors"], pos)

        self.current_pos = (0, 0)
        self.doors_locked = False
        self.boss_unlocked = False

    def load_sprite(self, name, filename):
        path = asset_path(filename)
        try:
            img = pygame.image.load(path).convert_alpha()
            self.sprites[name] = img
        except (FileNotFoundError, pygame.error) as exc:
            print(f"[Dungeon] Не удалось загрузить текстуру '{filename}' ({path}): {exc}. "
                  f"Использую запасную отрисовку.")
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

    def mark_shop_opened(self):
        self.rooms[self.current_pos]["shop_opened"] = True

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

    def draw(self, screen, player=None):
        matrix = self.get_matrix()
        room_type = self.rooms[self.current_pos]["type"]

        floor_color = SHOP_BG_COLOR if room_type == "shop" else BLACK
        pygame.draw.rect(screen, floor_color, (0, ARENA_Y, WIDTH, ARENA_HEIGHT))

        for r in range(ROWS):
            for c in range(COLS):
                tile = matrix[r][c]
                if tile in (TILE_EMPTY, TILE_BUSH, TILE_SHOP):
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

        if room_type == "shop":
            self._draw_chest(screen, player)

    def _draw_chest(self, screen, player):
        shop_rects = self.get_shop_rects()
        if not shop_rects:
            return

        left = min(r.x for r in shop_rects)
        top = min(r.y for r in shop_rects)
        bottom = max(r.bottom for r in shop_rects)
        center_y = (top + bottom) // 2

        is_open = self.rooms[self.current_pos].get("shop_opened", False)

        sprite_key = "chest_open" if is_open else "chest_closed"
        sprite = self.sprites.get(sprite_key)

        if sprite:
            x = left
            y = center_y - sprite.get_height() // 2
            screen.blit(sprite, (x, y))
        else:
            for rect in shop_rects:
                color = COIN_COLOR if is_open else (139, 69, 19)
                pygame.draw.rect(screen, (139, 69, 19), rect)
                pygame.draw.rect(screen, color, rect, 1)

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