# ui/interface.py

import pygame
from settings import *


class UI:
    def __init__(self):
        self.font_sm = pygame.font.SysFont("arial", 10, bold=True)
        self.font_md = pygame.font.SysFont("arial", 14, bold=True)
        self.font_lg = pygame.font.SysFont("arial", 22, bold=True)
        self.font_title = pygame.font.SysFont("arial", 28, bold=True)

    def draw_menu_background(self, screen):
        screen.fill(BLACK)
        for x in range(0, WIDTH, TILE_SIZE * 2):
            pygame.draw.line(screen, (25, 25, 30), (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILE_SIZE * 2):
            pygame.draw.line(screen, (25, 25, 30), (0, y), (WIDTH, y))

    def draw_main_menu(self, screen, current_page, selected_index, statistics=None):
        self.draw_menu_background(screen)

        if current_page == "main":
            title = self.font_title.render("МИР ТАНКОФФ", True, PLAYER_COLOR)
            screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 6))

            options = ["НАЧАТЬ ИГРУ", "СТАТИСТИКА", "НАСТРОЙКИ", "ВЫХОД"]
            for i, option in enumerate(options):
                selected = i == selected_index
                color = COIN_COLOR if selected else (170, 170, 170)
                text = f"> {option} <" if selected else option
                render = self.font_md.render(text, True, color)
                screen.blit(render, (WIDTH // 2 - render.get_width() // 2, HEIGHT // 2 + i * 22))

            controls = self.font_sm.render("W/S  ENTER", True, (120, 120, 120))
            screen.blit(controls, (WIDTH // 2 - controls.get_width() // 2, HEIGHT - 16))

        elif current_page == "statistics":
            title = self.font_lg.render("СТАТИСТИКА", True, WHITE)
            screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 12))

            if statistics is None:
                statistics = {
                    "games": 0, "wins": 0, "losses": 0,
                    "best_score": 0, "avg_score": 0,
                    "enemies": 0, "bosses": 0,
                }

            rows = [
                ("Игр", statistics["games"]),
                ("Побед", statistics["wins"]),
                ("Поражений", statistics["losses"]),
                ("Лучший", statistics["best_score"]),
                ("Средний", statistics["avg_score"]),
                ("Врагов", statistics["enemies"]),
                ("Боссов", statistics["bosses"]),
            ]

            y = 40
            for name, value in rows:
                left = self.font_sm.render(name, True, WHITE)
                right = self.font_sm.render(str(value), True, COIN_COLOR)
                screen.blit(left, (20, y))
                screen.blit(right, (WIDTH - 20 - right.get_width(), y))
                y += 16

            back = self.font_sm.render("ESC", True, RED)
            screen.blit(back, (WIDTH // 2 - back.get_width() // 2, HEIGHT - 14))

        elif current_page == "settings":
            title = self.font_lg.render("НАСТРОЙКИ", True, WHITE)
            screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 16))

            music = "ВКЛ" if GAME_SETTINGS["music"] else "ВЫКЛ"
            sounds = "ВКЛ" if GAME_SETTINGS["sounds"] else "ВЫКЛ"
            settings = [
                f"МУЗЫКА: {music}",
                f"ЗВУКИ: {sounds}",
                f"СЛОЖНОСТЬ: {GAME_SETTINGS['difficulty']}",
                "НАЗАД",
            ]

            for i, option in enumerate(settings):
                selected = i == selected_index
                color = COIN_COLOR if selected else (170, 170, 170)
                text = f"> {option} <" if selected else option
                render = self.font_sm.render(text, True, color)
                screen.blit(render, (WIDTH // 2 - render.get_width() // 2, 50 + i * 20))

            back = self.font_sm.render("ESC", True, RED)
            screen.blit(back, (WIDTH // 2 - back.get_width() // 2, HEIGHT - 14))

    def draw_hud(self, screen, player, dungeon):
        """HUD bar strictly above the 13×13 arena."""
        pygame.draw.rect(screen, UI_BG, (0, 0, WIDTH, UI_HEIGHT))
        pygame.draw.line(screen, (60, 60, 70), (0, UI_HEIGHT), (WIDTH, UI_HEIGHT), 1)

        for i in range(player.hp):
            x = 6 + i * 12
            pygame.draw.circle(screen, HEART_COLOR, (x, UI_HEIGHT // 2), 5)
            pygame.draw.circle(screen, (200, 30, 50), (x, UI_HEIGHT // 2), 3)

        score_text = self.font_sm.render(f"{player.score}", True, WHITE)
        screen.blit(score_text, (WIDTH - score_text.get_width() - 6, 3))

        if dungeon.doors_locked:
            battle_text = self.font_sm.render("БОЙ!", True, RED)
            screen.blit(battle_text, (WIDTH // 2 - battle_text.get_width() // 2, ARENA_Y + ARENA_HEIGHT - 12))

    def draw_shop_tooltip(self, screen, player):
        if player.hp >= PLAYER_MAX_HP:
            text = "HP полное"
        else:
            text = "E — бесплатное лечение"

        render = self.font_sm.render(text, True, WHITE)
        bg = pygame.Surface((render.get_width() + 8, render.get_height() + 4), pygame.SRCALPHA)
        bg.fill((40, 40, 50, 200))
        screen.blit(bg, (WIDTH // 2 - bg.get_width() // 2, ARENA_Y + 4))
        screen.blit(render, (WIDTH // 2 - render.get_width() // 2, ARENA_Y + 6))

    def draw_overlay(self, screen, state, score):
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))

        if state == STATE_GAME_OVER:
            title = self.font_lg.render("ПОРАЖЕНИЕ", True, RED)
        else:
            title = self.font_lg.render("ПОБЕДА!", True, GREEN)

        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 3))
        score_text = self.font_md.render(f"Счёт: {score}", True, WHITE)
        screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2))
        hint = self.font_sm.render("ENTER / ESC", True, (200, 200, 200))
        screen.blit(hint, (WIDTH // 2 - hint.get_width() // 2, HEIGHT // 2 + 24))

    def draw_confirm_exit(self, screen):
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        screen.blit(overlay, (0, 0))

        text = self.font_md.render("Выйти?", True, WHITE)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - 20))
        yes = self.font_sm.render("ENTER", True, GREEN)
        no = self.font_sm.render("ESC", True, RED)
        screen.blit(yes, (WIDTH // 2 - 40, HEIGHT // 2 + 4))
        screen.blit(no, (WIDTH // 2 + 10, HEIGHT // 2 + 4))
