# ui/interface.py

import pygame
from settings import *


class UI:
    def __init__(self):
        self.font_sm = pygame.font.SysFont("arial", 16, bold=True)
        self.font_md = pygame.font.SysFont("arial", 24, bold=True)
        self.font_lg = pygame.font.SysFont("arial", 64, bold=True)
        self.font_title = pygame.font.SysFont("arial", 80, bold=True)

    def draw_menu_background(self, screen):
        screen.fill(BLACK)

        for x in range(0, WIDTH, TILE_SIZE * 2):
            pygame.draw.line(screen, (25, 25, 30), (x, 0), (x, HEIGHT))

        for y in range(0, HEIGHT, TILE_SIZE * 2):
            pygame.draw.line(screen, (25, 25, 30), (0, y), (WIDTH, y))

    def draw_main_menu(self, screen, current_page, selected_index, statistics=None):
        self.draw_menu_background(screen)

        if current_page == "main":

            title_shadow = self.font_title.render("МИР ТАНКОФФ", True, (40, 0, 40))
            title = self.font_title.render("МИР ТАНКОФФ", True, PLAYER_COLOR)

            screen.blit(
                title_shadow,
                (WIDTH // 2 - title_shadow.get_width() // 2 + 4,
                 HEIGHT // 4 + 4)
            )

            screen.blit(
                title,
                (WIDTH // 2 - title.get_width() // 2,
                 HEIGHT // 4)
            )

            options = [
                "НАЧАТЬ ИГРУ",
                "СТАТИСТИКА",
                "НАСТРОЙКИ",
                "ВЫХОД"
            ]

            for i, option in enumerate(options):

                selected = i == selected_index

                color = COIN_COLOR if selected else (170, 170, 170)

                text = f"> {option} <" if selected else option

                render = self.font_md.render(text, True, color)

                screen.blit(
                    render,
                    (
                        WIDTH // 2 - render.get_width() // 2,
                        HEIGHT // 2 + i * 60,
                    )
                )

            controls = self.font_sm.render(
                "W/S или ↑↓   ENTER — выбрать",
                True,
                (120, 120, 120),
            )

            screen.blit(
                controls,
                (
                    WIDTH // 2 - controls.get_width() // 2,
                    HEIGHT - 40,
                )
            )

        elif current_page == "statistics":
            title = self.font_lg.render("СТАТИСТИКА", True, WHITE)
            screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 70))

            # Прямоугольник по центру
            rect_width = 600
            rect_x = WIDTH // 2 - rect_width // 2   # теперь ровно по центру
            rect_y = 165
            rect_height = 360
            pygame.draw.rect(screen, (30, 30, 35), (rect_x, rect_y, rect_width, rect_height), border_radius=10)
            pygame.draw.rect(screen, PLAYER_COLOR, (rect_x, rect_y, rect_width, rect_height), 2, border_radius=10)

            if statistics is None:
                statistics = {
                    "games": 0, "wins": 0, "losses": 0,
                    "best_score": 0, "avg_score": 0,
                    "coins": 0, "enemies": 0, "bosses": 0
                }

            rows = [
                ("Игр сыграно", statistics["games"]),
                ("Побед", statistics["wins"]),
                ("Поражений", statistics["losses"]),
                ("Лучший счёт", statistics["best_score"]),
                ("Средний счёт", statistics["avg_score"]),
                ("Монет собрано", statistics["coins"]),
                ("Врагов уничтожено", statistics["enemies"]),
                ("Боссов побеждено", statistics["bosses"]),
            ]

            y = rect_y + 25
            left_x = rect_x + 30          # отступ слева
            right_x = rect_x + rect_width - 80   # отступ справа, числа будут прижаты к правому краю

            for name, value in rows:
                left = self.font_md.render(name, True, WHITE)
                right = self.font_md.render(str(value), True, COIN_COLOR)
                screen.blit(left, (left_x, y))
                # Прижимаем число к правому краю (отнимаем ширину текста)
                screen.blit(right, (right_x - right.get_width(), y))
                y += 38

            back = self.font_sm.render("ESC — назад", True, RED)
            screen.blit(back, (WIDTH // 2 - back.get_width() // 2, HEIGHT - 45)
        )

        elif current_page == "settings":

            title = self.font_lg.render(
                "НАСТРОЙКИ",
                True,
                WHITE,
            )

            screen.blit(
                title,
                (
                    WIDTH // 2 - title.get_width() // 2,
                    90,
                )
            )

            music = "ВКЛ" if GAME_SETTINGS["music"] else "ВЫКЛ"
            sounds = "ВКЛ" if GAME_SETTINGS["sounds"] else "ВЫКЛ"

            settings = [
                f"МУЗЫКА: {music}",
                f"ЗВУКИ: {sounds}",
                f"СЛОЖНОСТЬ: {GAME_SETTINGS['difficulty']}",
                "СОХРАНИТЬ И НАЗАД",
            ]

            for i, option in enumerate(settings):

                selected = i == selected_index

                color = COIN_COLOR if selected else (170, 170, 170)

                text = f"> {option} <" if selected else option

                render = self.font_md.render(text, True, color)

                screen.blit(
                    render,
                    (
                        WIDTH // 2 - render.get_width() // 2,
                        240 + i * 60,
                    )
                )

            back = self.font_sm.render(
                "ESC — назад",
                True,
                RED,
            )

            screen.blit(
                back,
                (
                    WIDTH // 2 - back.get_width() // 2,
                    HEIGHT - 45,
                )
            )

    # ------------------- НОВЫЕ МЕТОДЫ (добавлены с правильным отступом) -------------------

    def draw_hud(self, screen, player, dungeon):
        """Верхняя панель с HP, монетами, очками и номером комнаты"""
        pygame.draw.rect(screen, UI_BG, (0, 0, WIDTH, UI_HEIGHT))
        pygame.draw.line(screen, (60, 60, 70), (0, UI_HEIGHT), (WIDTH, UI_HEIGHT), 2)

        # Здоровье (сердечки)
        for i in range(player.hp):
            x = 20 + i * 30
            y = 15
            pygame.draw.circle(screen, HEART_COLOR, (x + 10, y + 10), 10)
            pygame.draw.circle(screen, (200, 30, 50), (x + 10, y + 10), 8)

        # Монеты
        coin_text = self.font_md.render(f"🪙 {player.coins}", True, COIN_COLOR)
        screen.blit(coin_text, (WIDTH // 2 - 80, 15))

        # Очки
        score_text = self.font_md.render(f"⭐ {player.score}", True, WHITE)
        screen.blit(score_text, (WIDTH // 2 + 80, 15))

        # Номер комнаты (позиция в лабиринте)
        pos = dungeon.current_pos
        room_text = self.font_sm.render(f"Комната ({pos[0]}, {pos[1]})", True, (180, 180, 180))
        screen.blit(room_text, (WIDTH - 160, 20))

        # Если двери заперты – индикатор битвы
        if dungeon.doors_locked:
            battle_text = self.font_sm.render("⚔️ БОЙ!", True, RED)
            screen.blit(battle_text, (WIDTH // 2 - 40, 40))

    def draw_shop_tooltip(self, screen, player):
        """Подсказка при взаимодействии с магазином"""
        # Увеличиваем ширину до 320 и поднимаем выше
        tooltip_rect = pygame.Rect(WIDTH // 2 - 160, UI_HEIGHT + 10, 320, 60)
        pygame.draw.rect(screen, (40, 40, 50), tooltip_rect, border_radius=8)
        pygame.draw.rect(screen, COIN_COLOR, tooltip_rect, 2, border_radius=8)

        if player.coins < HEAL_COST:
            text = f"Не хватает монет (нужно {HEAL_COST})"
        elif player.hp >= PLAYER_MAX_HP:
            text = "HP уже полное"
        else:
            text = f"Нажмите E для лечения ({HEAL_COST} монет)"

        render = self.font_sm.render(text, True, WHITE)
        screen.blit(render, (WIDTH // 2 - render.get_width() // 2, UI_HEIGHT + 25))

    def draw_overlay(self, screen, state, score):
        """Затемнение и текст победы/поражения"""
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))

        if state == STATE_GAME_OVER:
            title = self.font_lg.render("ПОРАЖЕНИЕ", True, RED)
        else:  # STATE_VICTORY
            title = self.font_lg.render("ПОБЕДА!", True, GREEN)

        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 3))

        score_text = self.font_md.render(f"Счёт: {score}", True, WHITE)
        screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2))

        hint = self.font_sm.render("Нажмите ENTER или ESC для выхода в меню", True, (200, 200, 200))
        screen.blit(hint, (WIDTH // 2 - hint.get_width() // 2, HEIGHT // 2 + 60))

    def draw_confirm_exit(self, screen):
        """Диалог подтверждения выхода в меню"""
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        screen.blit(overlay, (0, 0))

        box = pygame.Rect(WIDTH // 2 - 200, HEIGHT // 2 - 60, 400, 120)
        pygame.draw.rect(screen, (50, 50, 60), box, border_radius=12)
        pygame.draw.rect(screen, WHITE, box, 2, border_radius=12)

        text = self.font_md.render("Выйти в меню?", True, WHITE)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - 30))

        yes = self.font_sm.render("ENTER — да", True, GREEN)
        no = self.font_sm.render("ESC — нет", True, RED)
        screen.blit(yes, (WIDTH // 2 - 100, HEIGHT // 2 + 20))
        screen.blit(no, (WIDTH // 2 + 20, HEIGHT // 2 + 20))