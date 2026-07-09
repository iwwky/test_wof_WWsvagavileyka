# ui/interface.py

import math
import random

import pygame

from settings import *


def _load_font(filename, size, fallback_name="arial"):
    path = font_path(filename)
    try:
        return pygame.font.Font(path, size)
    except (FileNotFoundError, pygame.error):
        return pygame.font.SysFont(fallback_name, size, bold=True)


class UI:
    def __init__(self):
        self.font_xs = _load_font("Tiny5.ttf", 7)
        self.font_sm = _load_font("Tiny5.ttf", 8)
        self.font_md = _load_font("Tiny5.ttf", 14)
        self.font_lg = _load_font("Tiny5.ttf", 22)
        self.font_title = _load_font("Tiny5.ttf", 26)

        self._menu_stars = [
            (random.randint(0, WIDTH), random.randint(0, HEIGHT), random.uniform(0.4, 1.0))
            for _ in range(40)
        ]
        self._menu_tick = 0

        heart_texture = self._load_optional_image("сердце.png")
        if heart_texture:
            self._heart_full = heart_texture
            self._heart_empty = self._make_empty_heart(heart_texture)
        else:
            self._heart_full = self._make_heart_icon(HEART_COLOR, filled=True)
            self._heart_empty = self._make_heart_icon((70, 70, 80), filled=False)

        self._coin_icon = self._make_coin_icon()
        self._star_icon = self._make_star_icon()

    @staticmethod
    def _load_optional_image(filename):
        try:
            return pygame.image.load(asset_path(filename)).convert_alpha()
        except (FileNotFoundError, pygame.error):
            return None

    @staticmethod
    def _make_empty_heart(full_heart):
        empty = full_heart.copy()
        empty.fill((70, 70, 80, 255), special_flags=pygame.BLEND_RGBA_MULT)
        return empty

    @staticmethod
    def _make_heart_icon(color, filled=True):
        surf = pygame.Surface((14, 14), pygame.SRCALPHA)
        cx, cy = 7, 8
        pygame.draw.circle(surf, color, (cx - 3, cy - 2), 3)
        pygame.draw.circle(surf, color, (cx + 3, cy - 2), 3)
        pygame.draw.polygon(surf, color, [(cx - 6, cy - 1), (cx + 6, cy - 1), (cx, cy + 6)])
        if not filled:
            pygame.draw.rect(surf, UI_BG, (2, 4, 10, 8))
            pygame.draw.circle(surf, color, (cx - 3, cy - 2), 3, 1)
            pygame.draw.circle(surf, color, (cx + 3, cy - 2), 3, 1)
            pygame.draw.polygon(surf, color, [(cx - 6, cy - 1), (cx + 6, cy - 1), (cx, cy + 6)], 1)
        return surf

    @staticmethod
    def _make_coin_icon():
        try:
            img = pygame.image.load(asset_path("монета.png")).convert_alpha()
            return pygame.transform.scale(img, (12, 12))
        except FileNotFoundError:
            surf = pygame.Surface((12, 12), pygame.SRCALPHA)
            pygame.draw.circle(surf, COIN_COLOR, (6, 6), 5)
            pygame.draw.circle(surf, (200, 150, 0), (6, 6), 3)
            return surf

    @staticmethod
    def _make_star_icon():
        try:
            img = pygame.image.load(asset_path("опыт.png")).convert_alpha()
            return pygame.transform.scale(img, (12, 12))
        except FileNotFoundError:
            surf = pygame.Surface((12, 12), pygame.SRCALPHA)
            points = []
            for i in range(5):
                angle = math.radians(-90 + i * 72)
                points.append((6 + 5 * math.cos(angle), 6 + 5 * math.sin(angle)))
                angle = math.radians(-90 + i * 72 + 36)
                points.append((6 + 2 * math.cos(angle), 6 + 2 * math.sin(angle)))
            pygame.draw.polygon(surf, UI_ACCENT, points)
            return surf

    def _draw_text_shadow(self, screen, font, text, color, pos, shadow=(2, 2)):
        shadow_surf = font.render(text, True, (0, 0, 0))
        text_surf = font.render(text, True, color)
        x, y = pos
        screen.blit(shadow_surf, (x + shadow[0], y + shadow[1]))
        screen.blit(text_surf, (x, y))
        return text_surf.get_width(), text_surf.get_height()

    def draw_menu_background(self, screen):
        screen.fill(BLACK)
        self._menu_tick += 1

        for i, (sx, sy, brightness) in enumerate(self._menu_stars):
            pulse = 0.5 + 0.5 * math.sin(self._menu_tick * 0.03 + i)
            c = int(80 + 120 * brightness * pulse)
            pygame.draw.circle(screen, (c // 3, c // 4, c), (sx, sy), 1)

        for x in range(0, WIDTH, TILE_SIZE):
            pygame.draw.line(screen, (20, 24, 36), (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILE_SIZE):
            pygame.draw.line(screen, (20, 24, 36), (0, y), (WIDTH, y))

        vignette = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        for y in range(HEIGHT):
            alpha = int(40 * (abs(y - HEIGHT // 2) / (HEIGHT // 2)))
            pygame.draw.line(vignette, (0, 0, 0, alpha), (0, y), (WIDTH, y))
        screen.blit(vignette, (0, 0))

    def _draw_menu_button(self, screen, text, y, selected):
        btn_w, btn_h = 170, 22
        btn_x = WIDTH // 2 - btn_w // 2

        if selected:
            glow = pygame.Surface((btn_w + 8, btn_h + 8), pygame.SRCALPHA)
            pygame.draw.rect(glow, (*UI_ACCENT, 40), glow.get_rect(), border_radius=6)
            screen.blit(glow, (btn_x - 4, y - 4))
            bg_color = (45, 52, 72)
            border_color = UI_ACCENT
            text_color = UI_ACCENT
        else:
            bg_color = UI_PANEL
            border_color = (60, 68, 90)
            text_color = (170, 175, 190)

        pygame.draw.rect(screen, bg_color, (btn_x, y, btn_w, btn_h), border_radius=4)
        pygame.draw.rect(screen, border_color, (btn_x, y, btn_w, btn_h), 1, border_radius=4)

        render = self.font_sm.render(text, True, text_color)
        screen.blit(render, (btn_x + btn_w // 2 - render.get_width() // 2, y + 6))

    def draw_main_menu(
        self,
        screen,
        current_page,
        selected_index,
        statistics=None,
        stat_filter="ВСЕ",
        score_history=None,
        recent_games=None,
    ):
        self.draw_menu_background(screen)

        if current_page == "main":
            title_y = 28
            self._draw_text_shadow(screen, self.font_title, "МИР", PLAYER_COLOR, (WIDTH // 2 - 25, title_y))
            self._draw_text_shadow(screen, self.font_title, "ТАНКОФФ", COIN_COLOR, (WIDTH // 2 - 58, title_y + 28))

            options = ["НАЧАТЬ", "СТАТИСТИКА", "НАСТРОЙКИ", "ВЫХОД"]
            start_y = 100
            for i, option in enumerate(options):
                self._draw_menu_button(screen, option, start_y + i * 28, i == selected_index)

            controls = self.font_xs.render("↑↓ ENTER", True, (100, 105, 120))
            screen.blit(controls, (WIDTH // 2 - controls.get_width() // 2, HEIGHT - 14))

        elif current_page == "statistics":
            self._draw_statistics_page(
                screen,
                statistics,
                stat_filter,
                score_history or [],
                recent_games or [],
            )

        elif current_page == "settings":
            self._draw_text_shadow(screen, self.font_lg, "НАСТРОЙКИ", WHITE, (WIDTH // 2 - 58, 16))

            music = "ВКЛ" if GAME_SETTINGS["music"] else "ВЫКЛ"
            sounds = "ВКЛ" if GAME_SETTINGS["sounds"] else "ВЫКЛ"
            fullscreen = "ВКЛ" if GAME_SETTINGS.get("fullscreen") else "ВЫКЛ"

            settings = [
                f"МУЗЫКА {music}",
                f"ЗВУК {sounds}",
                f"СЛОЖН. {GAME_SETTINGS['difficulty'][:3]}",
                f"ЭКРАН {fullscreen}",
                "НАЗАД",
            ]

            for i, option in enumerate(settings):
                self._draw_menu_button(screen, option, 52 + i * 26, i == selected_index)

            controls = self.font_xs.render("ENTER ESC", True, (100, 105, 120))
            screen.blit(controls, (WIDTH // 2 - controls.get_width() // 2, HEIGHT - 14))

    def _draw_statistics_page(self, screen, statistics, stat_filter, score_history, recent_games):
        self._draw_text_shadow(screen, self.font_lg, "СТАТ.", WHITE, (WIDTH // 2 - 30, 12))

        filter_text = self.font_sm.render(f"< {stat_filter[:6]} >", True, UI_ACCENT)
        screen.blit(filter_text, (WIDTH // 2 - filter_text.get_width() // 2, 38))

        if statistics is None:
            statistics = {
                "games": 0, "wins": 0, "losses": 0,
                "best_score": 0, "avg_score": 0,
                "coins": 0, "enemies": 0, "bosses": 0,
            }

        panel = pygame.Rect(8, 58, WIDTH - 16, 120)
        pygame.draw.rect(screen, UI_PANEL, panel, border_radius=4)
        pygame.draw.rect(screen, UI_ACCENT, panel, 1, border_radius=4)

        rows = [
            ("Игр", statistics["games"]),
            ("Побед", statistics["wins"]),
            ("Пораж.", statistics["losses"]),
            ("Рекорд", statistics["best_score"]),
            ("Монет", statistics["coins"]),
        ]

        y = panel.y + 8
        for name, value in rows:
            left = self.font_xs.render(name, True, WHITE)
            right = self.font_xs.render(str(value), True, COIN_COLOR)
            screen.blit(left, (panel.x + 8, y))
            screen.blit(right, (panel.right - right.get_width() - 8, y))
            y += 14

        self._draw_score_chart(screen, 12, 186, WIDTH - 24, 36, score_history)

        back = self.font_xs.render("←→ ESC", True, RED)
        screen.blit(back, (WIDTH // 2 - back.get_width() // 2, HEIGHT - 12))

    def _draw_score_chart(self, screen, x, y, width, height, score_history):
        pygame.draw.rect(screen, (18, 20, 30), (x, y, width, height), border_radius=3)
        pygame.draw.rect(screen, (60, 68, 90), (x, y, width, height), 1, border_radius=3)

        if not score_history:
            empty = self.font_xs.render("нет данных", True, (100, 105, 120))
            screen.blit(empty, (x + width // 2 - empty.get_width() // 2, y + height // 2 - 4))
            return

        scores = [row[0] for row in score_history]
        max_score = max(scores) or 1
        bar_width = max(6, (width - 16) // max(len(scores), 1) - 4)

        for index, row in enumerate(score_history):
            score = row[0]
            victory = row[1]
            bar_height = max(2, int((score / max_score) * (height - 10)))
            bar_x = x + 8 + index * (bar_width + 4)
            bar_y = y + height - bar_height - 4
            color = GREEN if victory else RED
            pygame.draw.rect(screen, color, (bar_x, bar_y, bar_width, bar_height), border_radius=2)

    def draw_hud(self, screen, player, dungeon):
        pygame.draw.rect(screen, UI_BG, (0, 0, WIDTH, UI_HEIGHT))
        pygame.draw.line(screen, UI_ACCENT, (0, UI_HEIGHT - 1), (WIDTH, UI_HEIGHT - 1), 2)

        heart_spacing = self._heart_full.get_width() - 2
        for i in range(player.max_hp):
            icon = self._heart_full if i < player.hp else self._heart_empty
            screen.blit(icon, (4 + i * heart_spacing, 4))

        score_text = self.font_sm.render(str(player.score), True, WHITE)
        score_x = WIDTH - 6 - score_text.get_width()
        screen.blit(score_text, (score_x, 8))

        star_x = score_x - self._star_icon.get_width() - 3
        screen.blit(self._star_icon, (star_x, 6))

        coin_text = self.font_sm.render(str(player.coins), True, COIN_COLOR)
        coin_text_x = star_x - 8 - coin_text.get_width()
        screen.blit(coin_text, (coin_text_x, 8))

        coin_icon_x = coin_text_x - self._coin_icon.get_width() - 3
        screen.blit(self._coin_icon, (coin_icon_x, 6))

    def draw_shop_tooltip(self, screen, player, locked=False):
        heal_cost = get_heal_cost()
        tooltip_w = 180
        tooltip_rect = pygame.Rect(WIDTH // 2 - tooltip_w // 2, ARENA_Y + 4, tooltip_w, 28)

        pygame.draw.rect(screen, UI_PANEL, tooltip_rect, border_radius=4)
        pygame.draw.rect(screen, COIN_COLOR, tooltip_rect, 1, border_radius=4)

        if locked:
            text = "Сначала победите врагов"
        elif player.coins < heal_cost:
            text = f"Нужно {heal_cost} монет"
        elif player.hp >= player.max_hp:
            text = "HP полное"
        else:
            text = f"E — лечение ({heal_cost})"

        render = self.font_xs.render(text, True, WHITE)
        screen.blit(render, (tooltip_rect.centerx - render.get_width() // 2, tooltip_rect.centery - 4))

    def draw_overlay(self, screen, state, score):
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 190))
        screen.blit(overlay, (0, 0))

        if state == STATE_GAME_OVER:
            title = self.font_lg.render("ПОРАЖЕНИЕ", True, RED)
        else:
            title = self.font_lg.render("ПОБЕДА!", True, GREEN)

        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 3))
        score_text = self.font_md.render(f"Счёт: {score}", True, WHITE)
        screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2))
        hint = self.font_xs.render("ENTER / ESC", True, (180, 185, 200))
        screen.blit(hint, (WIDTH // 2 - hint.get_width() // 2, HEIGHT // 2 + 28))

    def draw_confirm_exit(self, screen):
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        screen.blit(overlay, (0, 0))

        box = pygame.Rect(WIDTH // 2 - 80, HEIGHT // 2 - 30, 160, 60)
        pygame.draw.rect(screen, UI_PANEL, box, border_radius=6)
        pygame.draw.rect(screen, WHITE, box, 1, border_radius=6)

        text = self.font_sm.render("Выйти?", True, WHITE)
        screen.blit(text, (box.centerx - text.get_width() // 2, box.y + 10))
        yes = self.font_xs.render("ENTER", True, GREEN)
        no = self.font_xs.render("ESC", True, RED)
        screen.blit(yes, (box.centerx - 36, box.bottom - 18))
        screen.blit(no, (box.centerx + 8, box.bottom - 18))