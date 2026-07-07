# main.py
import pygame
import sys
import time
from settings import *
from core.dungeon import Dungeon
from entities.player import Player
from entities.enemy import Enemy
from ui.interface import UI
from data.database import Database
from data.save_manager import load_settings, save_settings


class GameApp:
    def __init__(self):
        pygame.init()
        GAME_SETTINGS.update(load_settings())

        self.window_size = (WIDTH * DEFAULT_WINDOW_SCALE, HEIGHT * DEFAULT_WINDOW_SCALE)
        self.screen = pygame.display.set_mode(self.window_size, pygame.RESIZABLE)
        pygame.display.set_caption("Мир Танкофф")

        self.game_surface = pygame.Surface((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.ui = UI()
        self.database = Database()

        self.state = STATE_MENU
        self.menu_page = "main"
        self.menu_index = 0

        self.reset_game()

    def _present(self):
        win_w, win_h = self.screen.get_size()
        scale = min(win_w / WIDTH, win_h / HEIGHT)
        dest_w = max(1, int(WIDTH * scale))
        dest_h = max(1, int(HEIGHT * scale))
        scaled = pygame.transform.scale(self.game_surface, (dest_w, dest_h))
        self.screen.fill(BLACK)
        self.screen.blit(scaled, ((win_w - dest_w) // 2, (win_h - dest_h) // 2))

    def reset_game(self):
        self.dungeon = Dungeon()
        start_x = (COLS // 2) * TILE_SIZE
        start_y = (ROWS // 2) * TILE_SIZE
        self.player = Player(start_x, start_y)

        self.game_start_time = time.time()
        self.enemies_killed = 0
        self.bosses_killed = 0
        self.result_saved = False
        self.enemies = []
        self.bullets = []

        self.enter_room()

    def enter_room(self):
        self.bullets.clear()
        self.enemies.clear()
        room = self.dungeon.rooms[self.dungeon.current_pos]

        if not room["cleared"]:
            self.dungeon.lock_doors()

            if room["type"] == "arena":
                spawns = [
                    (2 * TILE_SIZE, 2 * TILE_SIZE),
                    ((COLS - 3) * TILE_SIZE, 2 * TILE_SIZE),
                    ((COLS // 2) * TILE_SIZE, (ROWS - 3) * TILE_SIZE),
                ]
                for sx, sy in spawns:
                    self.enemies.append(Enemy(sx, sy, is_boss=False))

            elif room["type"] == "boss":
                bx = (COLS // 2) * TILE_SIZE - BOSS_SIZE // 2 + TILE_SIZE // 2
                by = 3 * TILE_SIZE
                self.enemies.append(Enemy(bx, by, is_boss=True))

    def handle_room_transitions(self):
        if self.dungeon.doors_locked:
            return

        cx, cy = self.dungeon.current_pos
        col = self.player.grid_col()
        row = self.player.grid_row()
        transitioned = False

        if row == 0 and "top" in self.dungeon.rooms[(cx, cy)]["doors"]:
            self.dungeon.current_pos = (cx, cy + 1)
            self.player.y = (ROWS - 2) * TILE_SIZE
            transitioned = True
        elif row >= ROWS - 1 and "bottom" in self.dungeon.rooms[(cx, cy)]["doors"]:
            self.dungeon.current_pos = (cx, cy - 1)
            self.player.y = TILE_SIZE
            transitioned = True
        elif col == 0 and "left" in self.dungeon.rooms[(cx, cy)]["doors"]:
            self.dungeon.current_pos = (cx - 1, cy)
            self.player.x = (COLS - 2) * TILE_SIZE
            transitioned = True
        elif col >= COLS - 1 and "right" in self.dungeon.rooms[(cx, cy)]["doors"]:
            self.dungeon.current_pos = (cx + 1, cy)
            self.player.x = TILE_SIZE
            transitioned = True

        if transitioned:
            self.enter_room()

    def update_logic(self):
        keys = pygame.key.get_pressed()

        self.player.update(keys, self.dungeon, self.bullets, self.enemies)
        self.handle_room_transitions()

        for enemy in self.enemies:
            enemy.update(self.dungeon, self.bullets, self.player, self.enemies)

        for bullet in self.bullets[:]:
            bullet.update(self.dungeon)
            if not bullet.active:
                self.bullets.remove(bullet)
                continue

            if bullet.is_player:
                for enemy in self.enemies[:]:
                    center_x = enemy.x + enemy.size // 2
                    center_y = enemy.y + enemy.size // 2
                    if (bullet.x - center_x) ** 2 + (bullet.y - center_y) ** 2 < (enemy.size // 2 + bullet.radius) ** 2:
                        enemy.hp -= 1
                        bullet.active = False
                        if enemy.hp <= 0:
                            if enemy.is_boss:
                                self.bosses_killed += 1
                            else:
                                self.enemies_killed += 1
                            self.player.score += 500 if enemy.is_boss else 100
                            self.enemies.remove(enemy)
                        break
            else:
                if self.player.i_frames == 0:
                    center_x = self.player.x + self.player.size // 2
                    center_y = self.player.y + self.player.size // 2
                    if (bullet.x - center_x) ** 2 + (bullet.y - center_y) ** 2 < (self.player.size // 2 + bullet.radius) ** 2:
                        self.player.hp -= 1
                        self.player.i_frames = PLAYER_I_FRAMES
                        bullet.active = False
                        if self.player.hp <= 0:
                            self.state = STATE_GAME_OVER
                            self.save_game_result()

        if self.dungeon.doors_locked and len(self.enemies) == 0:
            self.dungeon.unlock_doors()
            if self.dungeon.rooms[self.dungeon.current_pos]["type"] == "boss":
                self.state = STATE_VICTORY
                self.save_game_result()

        all_cleared = all(
            room["cleared"] for pos, room in self.dungeon.rooms.items() if room["type"] == "arena"
        )
        self.dungeon.boss_unlocked = all_cleared

    def draw(self):
        self.game_surface.fill(BLACK)

        if self.state == STATE_MENU:
            stats = self.database.get_statistics()
            self.ui.draw_main_menu(self.game_surface, self.menu_page, self.menu_index, stats)
            self._present()
            return

        self.ui.draw_hud(self.game_surface, self.player, self.dungeon)
        self.dungeon.draw(self.game_surface)
        self.player.draw(self.game_surface)
        for enemy in self.enemies:
            enemy.draw(self.game_surface)
        for bullet in self.bullets:
            bullet.draw(self.game_surface)
        self.dungeon.draw_top_layer(self.game_surface)

        if self.dungeon.rooms[self.dungeon.current_pos]["type"] == "shop":
            player_rect = pygame.Rect(self.player.x, self.player.y + ARENA_Y, self.player.size, self.player.size)
            interaction_zone = player_rect.inflate(8, 8)
            for shop_rect in self.dungeon.get_shop_rects():
                if interaction_zone.colliderect(shop_rect):
                    self.ui.draw_shop_tooltip(self.game_surface, self.player)
                    break

        if self.state in (STATE_GAME_OVER, STATE_VICTORY):
            self.ui.draw_overlay(self.game_surface, self.state, self.player.score)

        if self.state == STATE_CONFIRM_EXIT:
            self.ui.draw_confirm_exit(self.game_surface)

        self._present()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.database.close()
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.VIDEORESIZE:
                    self.screen = pygame.display.set_mode(event.size, pygame.RESIZABLE)

                if event.type == pygame.KEYDOWN:
                    if self.state == STATE_MENU:
                        if event.key in (pygame.K_UP, pygame.K_w, 1094, 1062):
                            self.menu_index -= 1
                        elif event.key in (pygame.K_DOWN, pygame.K_s, 1099, 1067):
                            self.menu_index += 1
                        elif event.key == pygame.K_RETURN:
                            if self.menu_page == "main":
                                if self.menu_index == 0:
                                    self.reset_game()
                                    self.state = STATE_PLAYING
                                elif self.menu_index == 1:
                                    self.menu_page = "statistics"
                                    self.menu_index = 0
                                elif self.menu_index == 2:
                                    self.menu_page = "settings"
                                    self.menu_index = 0
                                elif self.menu_index == 3:
                                    self.database.close()
                                    pygame.quit()
                                    sys.exit()
                            elif self.menu_page == "settings":
                                if self.menu_index == 0:
                                    GAME_SETTINGS["music"] = not GAME_SETTINGS["music"]
                                    save_settings(GAME_SETTINGS)
                                elif self.menu_index == 1:
                                    GAME_SETTINGS["sounds"] = not GAME_SETTINGS["sounds"]
                                    save_settings(GAME_SETTINGS)
                                elif self.menu_index == 2:
                                    diffs = ["ЛЕГКАЯ", "СРЕДНЯЯ", "СЛОЖНАЯ"]
                                    cur = diffs.index(GAME_SETTINGS["difficulty"]) if GAME_SETTINGS["difficulty"] in diffs else 1
                                    GAME_SETTINGS["difficulty"] = diffs[(cur + 1) % 3]
                                    save_settings(GAME_SETTINGS)
                                elif self.menu_index == 3:
                                    self.menu_page = "main"
                                    self.menu_index = 0
                        elif event.key == pygame.K_ESCAPE:
                            if self.menu_page != "main":
                                self.menu_page = "main"
                                self.menu_index = 0

                        if self.menu_page == "main":
                            self.menu_index %= 4
                        elif self.menu_page == "settings":
                            self.menu_index %= 4
                        else:
                            self.menu_index = 0

                    elif self.state in (STATE_GAME_OVER, STATE_VICTORY):
                        if event.key in (pygame.K_RETURN, pygame.K_ESCAPE):
                            self.state = STATE_MENU
                            self.menu_page = "main"
                            self.menu_index = 0

                    elif self.state == STATE_PLAYING:
                        if event.key == pygame.K_ESCAPE:
                            self.state = STATE_CONFIRM_EXIT

                    elif self.state == STATE_CONFIRM_EXIT:
                        if event.key == pygame.K_ESCAPE:
                            self.state = STATE_PLAYING
                        elif event.key == pygame.K_RETURN:
                            self.state = STATE_MENU
                            self.menu_page = "main"
                            self.menu_index = 0

            if self.state == STATE_PLAYING:
                self.update_logic()

            self.draw()
            pygame.display.flip()
            self.clock.tick(FPS)

    def save_game_result(self):
        if self.result_saved or self.database is None:
            return

        play_time = time.time() - self.game_start_time
        self.database.add_result(
            difficulty=GAME_SETTINGS["difficulty"],
            score=self.player.score,
            coins=0,
            enemies=self.enemies_killed,
            bosses=self.bosses_killed,
            victory=self.state == STATE_VICTORY,
            play_time=play_time,
        )
        self.result_saved = True


if __name__ == "__main__":
    app = GameApp()
    app.run()
